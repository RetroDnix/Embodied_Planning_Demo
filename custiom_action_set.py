import inspect
import torch
from sentence_transformers import SentenceTransformer
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
from actions import ACTION_DICT  # Import your action dictionary
from actions import utils

@dataclass
class HighLevelAction:
    signature: str
    description: str
    examples: List[str]
    function: str
    add_code: bool

class CustomActionSet:
    """
    Custom action set for robot control that integrates with existing ACTION_DICT
    """
    # _instance = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(CustomActionSet, cls).__new__(cls)
    #         cls._instance._initialized = False
    #     return cls._instance
    

    def __init__(
        self,
        action_dict: Dict[str, List[Callable]] = None,
        safety_actions: Optional[List[Callable]] = None,
        retrieval_model_name: str = "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        demo_mode: bool = False,
        retrievable_actions: bool = False
    ):
        """
        Initialize with actions from ACTION_DICT or provided ones.

        Args:
            action_dict: Dictionary of action categories and functions
            safety_actions: Additional safety-related action functions
            retrieval_model_name: Name of the retrieval model
            demo_mode: Whether to run in demo mode
        """
        # if self._initialized:
        #     return
        self.demo_mode = demo_mode
        self.retrieval_model_name = retrieval_model_name
        self.python_includes = ""
        self.action_dict = action_dict or ACTION_DICT

        # Collect all actions
        self.base_actions = self.action_dict["base"]     # [func for category in self.action_dict.values() for func in category]
        self.base_actions.extend(safety_actions or [])
        self.retri_actions = self.action_dict["store"] 

        # Parse actions into high-level actions
        self.action_set: Dict[str, HighLevelAction] = {}
        self.retrievable_action_set: Dict[str, HighLevelAction] = {}

        self._parse_actions(self.base_actions, self.action_set)
        self._parse_actions(self.retri_actions, self.retrievable_action_set)


        self.python_includes += "import time\n"
        for _, func in inspect.getmembers(utils, inspect.isfunction):
            self.python_includes += f"""\
{inspect.getsource(func)}


"""
        # Build retrieval index if needed
        if retrievable_actions:
            self._build_retrieval_index()

    def _parse_actions(self, actions: List[Callable], action_set: Dict[str, HighLevelAction]) -> None:
        """Parse and register action functions."""
        for func in actions:
            if func.__name__ in action_set:
                continue

            source = inspect.getsource(func)
            self.python_includes += f"{source}\n\n"

            signature = f"{func.__name__}{inspect.signature(func)}"
            docstring = inspect.getdoc(func) or ""
            parts = docstring.split("Examples:", 1)
            description = parts[0].strip()
            examples = [ex.strip() for ex in parts[1].split("\n")[1:] if ex.strip()] if len(parts) > 1 else []

            action_set[func.__name__] = HighLevelAction(
                signature=signature,
                description=description,
                examples=examples,
                function=source,
                add_code=False
            )

    def _build_retrieval_index(self) -> None:
        """Initialize the action retrieval system."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.retrieval_model = SentenceTransformer(self.retrieval_model_name, trust_remote_code=True).to(self.device)

        # Prepare action descriptions for retrieval
        action_descriptions = [
            self.get_action_doc(action, with_long_description=True, with_examples=True)
            for action in self.retrievable_action_set.values()
        ]

        # Encode actions into embeddings
        self.action_embeddings = self.retrieval_model.encode(action_descriptions, convert_to_tensor=True)
        self.retri_action_list = list(self.retrievable_action_set.values())

    def retrieve_actions(self, query: str, top_k: int = 3) -> Dict[str, HighLevelAction]:
        """Retrieve the top-K relevant actions based on query."""
        query_embedding = self._get_query_embedding(query)
        scores = self._get_similarity_scores(query_embedding)
        top_indices = scores.topk(min(top_k, len(self.retri_action_list))).indices
        
        return {
            self.retri_action_list[i].signature.split('(')[0]: self.retri_action_list[i]
            for i in top_indices
        }

    def _get_query_embedding(self, query: str) -> torch.Tensor:
        """Encode the query into an embedding."""
        return self.retrieval_model.encode(query, convert_to_tensor=True)

    def _get_similarity_scores(self, query_embedding: torch.Tensor) -> torch.Tensor:
        """Calculate the similarity between query and action embeddings."""
        return torch.matmul(query_embedding, self.action_embeddings.T).squeeze()

    @staticmethod
    def get_action_doc(
        action: HighLevelAction, with_long_description: bool = True, with_examples: bool = True
    ) -> str:
        """Generate the documentation of an action."""
        if with_long_description and with_examples and action.add_code:
            return f"{action.function}\n"

        description = f"{action.signature}\n"
        if with_long_description:
            description += f"    Description: {action.description}\n"
        if with_examples and action.examples:
            description += "    Examples:\n" + "".join(f"        {ex}\n" for ex in action.examples) + "\n"
        return description

    def describe(
        self,
        with_long_description: bool = True,
        with_examples: bool = True,
        retrieval_query: Optional[str] = None,
        num_retrieve: int = 0
    ) -> str:
        """Describe all actions or a subset of actions retrieved by query."""
        action_set = self.action_set
        if retrieval_query and num_retrieve and self.retrievable_action_set:
            retrieved_actions = self.retrieve_actions(retrieval_query, num_retrieve)
            action_set = {**action_set, **retrieved_actions}

        description = f"\n{len(action_set)} different types of actions are available.\n\n"
        for _, action in action_set.items():
            description += self.get_action_doc(action, with_long_description, with_examples)

        return description

    def to_python_code(self, solution: str):
        python_code = ""
        python_code += self.python_includes
        main = f"""\
        
def main():
    solution()

if __name__ == "__main__":
    main()
"""
        return python_code + solution + main