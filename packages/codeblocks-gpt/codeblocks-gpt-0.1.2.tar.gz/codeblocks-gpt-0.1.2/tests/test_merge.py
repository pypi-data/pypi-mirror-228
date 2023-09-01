from codeblocks.parser.create import create_parser


def verify_merge(original_file, updated_file, expected_file, language):
    with open(original_file, 'r') as f:
        original_content = f.read()

    with open(updated_file, 'r') as f:
        updated_content = f.read()

    with open(expected_file, 'r') as f:
        expected_content = f.read()

    parser = create_parser(language)
    original_block = parser.parse(original_content)
    updated_block = parser.parse(updated_content)

    gpt_tweaks = original_block.merge(updated_block, first_level=True)

    print("gpt_tweaks: ", gpt_tweaks)
    print(original_block.to_string())
    assert original_block.to_string() == expected_content


def test_merge_java_insert_after_comment():
    verify_merge(
        "java/calculator.java",
        "java/calculator_insert1.java",
        "java/calculator_merged1.java",
        "java")


def test_merge_java_insert_before_comment():
    verify_merge(
        "java/calculator.java",
        "java/calculator_insert2.java",
        "java/calculator_merged2.java",
        "java")

def test_merge_java_replace():
    verify_merge(
        "java/calculator.java",
        "java/calculator_replace.java",
        "java/calculator_replace.java",
        "java")

def test_merge_java_book():
    verify_merge(
        "java/Book.java",
        "java/Book_add_field2.java",
        "java/Book_merged2.java",
        "java")


def test_merge_java_book_2():
    verify_merge(
        "java/Book.java",
        "java/Book_add_field3.java",
        "java/Book_merged2.java",
        "java")

def test_merge_python_insert_after_comment():
    verify_merge(
        "python/calculator.py",
        "python/calculator_insert1.py",
        "python/calculator_merged1.py",
        "python")


def test_merge_python_insert_before_comment():
    verify_merge(
        "python/calculator.py",
        "python/calculator_insert2.py",
        "python/calculator_merged2.py",
        "python")

def test_merge_python_replace():
    verify_merge(
        "python/calculator.py",
        "python/calculator_replace.py",
        "python/calculator_replace.py",
        "python")

def test_merge_python_sublist_update():
    verify_merge(
        "python/sublist.py",
        "python/sublist_update.py",
        "python/sublist_update.py",
        "python")

def test_merge_python_update_function():
    verify_merge(
        "python/affine_cipher.py",
        "python/affine_cipher_update_function.py",
        "python/affine_cipher_merged.py",
        "python")

def test_merge_python_update_function_2():
    verify_merge(
        "python/list_ops.py",
        "python/list_ops_update_function.py",
        "python/list_ops_merged.py",
        "python")

def test_merge_python_update_nested_function():
    verify_merge(
        "python/restapi.py",
        "python/restapi_updated_function.py",
        "python/restapi_merged.py",
        "python")

def test_merge_python_update_function_before_vars():
    verify_merge(
        "python/say.py",
        "python/say_update.py",
        "python/say_merged.py",
        "python")

def test_merge_typescript_react():
    verify_merge(
        "typescript/todo.tsx",
        "typescript/todo_add_filter.tsx",
        "typescript/todo_merged.tsx",
        "tsx")
