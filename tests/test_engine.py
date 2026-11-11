from engine import load_knowledge, retrieve, local_answer, tokenize

def test_knowledge_has_sources():
    assert all(row['source'].startswith('https://') for row in load_knowledge())

def test_retrieve_wash_sales():
    assert retrieve('What is a wash sale?')[0]['id'] == 'wash-sale'

def test_retrieve_chinese_rmd():
    assert retrieve('继承 IRA 有什么 RMD 规则？')[0]['id'] in ('inherited-ira', 'rmd')

def test_unknown_fallback():
    assert local_answer('quantum banana stargazing')['sources'] == []

def test_tokens():
    assert 'roth' in tokenize('Roth IRA 账户')
