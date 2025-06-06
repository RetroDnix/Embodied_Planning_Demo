import inspect
import openai
import torch
from sentence_transformers import SentenceTransformer
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
from actions import ACTION_DICT  # Import your action dictionary
from base import utils, vla, vlm
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

GPT_MODEL = 'Embedding-V1'

OPENAI_API_KEY = "sk-DRxEVD9NJPfTNZn9852f350063B249Dc9aD49503B1Ad70Ad"
OPENAI_API_BASE = "http://vip.ooo.cool/v1"

client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

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
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CustomActionSet, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    

    def __init__(
        self,
        action_dict: Dict[str, List[Callable]] = None,
        safety_actions: Optional[List[Callable]] = None,
        retrieval_model_name: str = "Alibaba-NLP/gte-Qwen2-1.5B-instruct",
        demo_mode: bool = False,
        retrievable_actions: bool = False,
        use_API: bool = False,
        print_log = False
    ):
        """
        Initialize with actions from ACTION_DICT or provided ones.

        Args:
            action_dict: Dictionary of action categories and functions
            safety_actions: Additional safety-related action functions
            retrieval_model_name: Name of the retrieval model
            demo_mode: Whether to run in demo mode
        """
        if self._initialized:
            print(f"use_API : {'True' if self.use_API else 'False'}")  # 正确的 Python 三元表达式
            return
        self._initialized = True
        self.demo_mode = demo_mode
        self.retrieval_model_name = retrieval_model_name
        self.python_includes = ""
        self.functions_includes = []
        self.action_dict = action_dict or ACTION_DICT
        # Collect all actions
        self.base_actions = self.action_dict["base"]    
        self.base_actions.extend(safety_actions or [])
        self.retri_actions = [x for x in self.action_dict["store"]  if x not in self.action_dict["base"] ] 

        # Parse actions into high-level actions
        self.action_set: Dict[str, HighLevelAction] = {}
        self.retrievable_action_set: Dict[str, HighLevelAction] = {}
        self.use_API=use_API
        self.print_log = print_log

        self.python_includes += "import time\n"
        for module in [utils, vla, vlm]:
            for _, func in inspect.getmembers(module, inspect.isfunction):
                self.functions_includes.append(func.__name__)
                self.python_includes += f"""\
{inspect.getsource(func)}


"""

        self._parse_actions(self.base_actions, self.action_set)
        self._parse_actions(self.retri_actions, self.retrievable_action_set)

        # Build retrieval index if needed
        if retrievable_actions:
            self._build_retrieval_index()

    def _parse_actions(self, actions: List[Callable], action_set: Dict[str, HighLevelAction]) -> None:
        """Parse and register action functions."""
        for func in actions:
            if func.__name__ in action_set:
                continue

            source = inspect.getsource(func)
            if func.__name__ not in self.functions_includes:
                self.functions_includes.append(func.__name__)
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
        if self.use_API:
            # Prepare action descriptions for retrieval
            action_descriptions = [
                self.get_action_doc(action, with_long_description=True, with_examples=True)
                for action in self.retrievable_action_set.values()
            ]
            # Encode actions into embeddings
            response = client.embeddings.create(input=action_descriptions, model=GPT_MODEL)
            self.action_embeddings = torch.tensor([record.embedding for record in response.data])
            self.retri_action_list = list(self.retrievable_action_set.values())
        else:
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
        # client.embeddings.create(input=[text], model=model).data[0].embedding
        query_embedding = self._get_query_embedding(query)
        scores = self._get_similarity_scores(query_embedding)
        top_indices = scores.topk(min(top_k, len(self.retri_action_list))).indices
        
        return {
            self.retri_action_list[i].signature.split('(')[0]: self.retri_action_list[i]
            for i in top_indices
        }

    def _get_query_embedding(self, query: str) -> torch.Tensor:
        """Encode the query into an embedding."""
        if self.use_API:
            return torch.Tensor(client.embeddings.create(input=[query], model=GPT_MODEL).data[0].embedding)
        return self.retrieval_model.encode(query, convert_to_tensor=True)

    def _get_similarity_scores(self, query_embedding: torch.Tensor) -> torch.Tensor:
        """Calculate the similarity between query and action embeddings."""
        return torch.matmul(query_embedding, self.action_embeddings.T).squeeze()

    def add_functions_from_strings(
        self,
        func_str_list: List[str],
        action_name_list: List[str],
        rebuild_index: bool = True,
        write_action_path: str = "actions/store.py",
    ) -> None:
        # 写入函数到文件
        try:
            with open(write_action_path, 'a+', encoding='utf-8') as fw:
                fw.write('\n\n' + '\n\n'.join(func_str_list))
        except IOError as e:
            print(f"写入文件失败: {str(e)}")
            return
        
        # 强制重新加载模块
        try:
            import importlib
            import sys
            if 'actions.store' in sys.modules:
                importlib.reload(sys.modules['actions.store'])
            store = importlib.import_module('actions.store')
        except ImportError as e:
            print(f"导入store模块失败: {str(e)}")
            return
        
        functions = []
        for name in action_name_list:
            try:
                f = getattr(store, name)
                if callable(f):
                    # 添加模块前缀检查（可选）
                    module = getattr(f, '__module__', '')
                    if module.startswith('actions.'):
                        functions.append(f)
                        if self.print_log:
                            print(f"成功获取函数: {name}")
                    else:
                        if self.print_log:
                            print(f"函数'{name}'模块前缀不匹配: {module}")
            except Exception as e:
                print(f"获取函数'{name}'失败: {str(e)}")
        
        if not functions:
            print("警告: 没有有效的函数被获取")
            return
        
        # 更新数据结构
        self.action_dict.setdefault("store", []).extend(functions)
        self.retri_actions.extend(functions)
        self._parse_actions(functions, self.retrievable_action_set)
        
        if rebuild_index and hasattr(self, 'action_embeddings'):
            try:
                self._build_retrieval_index()
            except Exception as e:
                print(f"重建检索索引失败: {str(e)}")
    
                
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
        num_retrieve: int = 0,
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

    def to_python_code(self, solution: str, traj_name: str):
        python_code = ""
        python_code += self.python_includes
        main = f"""\
        
def main():
    {traj_name}()

if __name__ == "__main__":
    main()
"""
        return python_code + solution + main
    
    def get_function_bodies_from_code(self, function_str: str) -> List[str]:
        import ast
        import re
        
        # 新增：提取代码块内容（```或```python ```包裹的部分）
        def extract_code_blocks(text):
            pattern = r'```(?:python)?\s*\n?(.*?)\n?```'
            matches = re.findall(pattern, text, re.DOTALL)
            return matches if matches else [text]  # 如果没有代码块，返回原始文本
        
        try:
            # 先提取所有代码块
            code_blocks = extract_code_blocks(function_str)
            all_function_bodies = []
            
            for block in code_blocks:
                # Parse the function string into an AST
                tree = ast.parse(block)
                
                # Extract all function calls
                all_function_calls = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        all_function_calls.add(node.func.id)
                
                # Filter out Python built-ins and standard library functions
                python_builtins = dir(__builtins__)
                custom_function_calls = [func for func in all_function_calls 
                                        if func not in python_builtins]
                
                # Get function bodies for the custom functions
                function_bodies = []
                
                for func_name in custom_function_calls:
                    # Check in the main action set
                    if func_name in self.retrievable_action_set:
                        function_bodies.append(self.retrievable_action_set[func_name].function)
                
                all_function_bodies.extend(function_bodies)

            # 打印调试信息
            for func in all_function_bodies and self.print_log:
                print("="*50)
                print(func)
                print("="*50)
                
            return all_function_bodies
            
        except SyntaxError as e:
            print(f"Syntax error in function string: {e}")
            return []
        except Exception as e:
            print(f"Error extracting function calls: {e}")
            return []