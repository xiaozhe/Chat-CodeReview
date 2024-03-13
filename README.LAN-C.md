

# tree-sitter

## install

install tree-sitter in python3 

```shell
pip3 install tree-sitter
```

## build my-languages.so

build c/cpp language by tree-sitter

- step 1 : create build environment
  
```shell
cd [your_path];
mkdir tree-sitter-build;
cd tree-sitter-build;
mkdir -p verdor/tree-sitter-c;
mkdir -p verdor/tree-sitter-cpp;
git clone https://github.com/tree-sitter/tree-sitter-c.git   ./verdor/tree-sitter-c   ;
git clone https://github.com/tree-sitter/tree-sitter-cpp.git ./verdor/tree-sitter-cpp ;

```

- step 2 : create build python file

[your_path]/tree-sitter-build/build.py

```python
from tree_sitter import Language

Language.build_library(

  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'vendor/tree-sitter-c',
    'vendor/tree-sitter-cpp'
    # 'vendor/tree-sitter-java',
    # 'vendor/tree-sitter-python',
    # 'vendor/tree-sitter-cpp',
  ]
)
```

- step 3 : build my-languages.so

```shell
cd [your_path]/tree-sitter-build;
python3 ./build.py ;
ls build ;
# you will get a file : my-languages.so
cp build/my-languages.so  /usr/lib/my-languages.so ;
```

## test my-languages.so

- step 1: create test python file

[your_path]/tree-sitter-build/test.py

```python
from tree_sitter import Language, Parser

CPP_LANGUAGE = Language('/usr/lib/my-languages.so', 'cpp')

# 举一个CPP例子
cpp_parser = Parser()
cpp_parser.set_language(CPP_LANGUAGE)

# 这是b站网友写的代码，解析看看
cpp_code_snippet = '''
int mian{
  piantf("hell world");
  remake O;
}
'''

# 没报错就是成功
tree = cpp_parser.parse(bytes(cpp_code_snippet, "utf8"))
# 注意，root_node 才是可遍历的树节点
root_node = tree.root_node

print(root_node)
print('ok')
```

- step 2: run test.py

```shell
cd [your_path]/tree-sitter-build;
python3 ./test.py ;
```

if you get next response, it's ok

```shell
<Node type=translation_unit, start_point(1,0), end_point=(5,0)>
ok
```