import json
from decimal import Decimal
import pytest
from farol.expenses.contracts import ContractError
from farol.expenses.http import extract, next_request, records_from


def test_array_envelope_rejects_html_and_application_errors():
    for value in ['<html>',{'success':False},{'dados':{}}]:
        with pytest.raises(ContractError): records_from(value,'dados')


def test_next_link_cannot_exfiltrate_authorization_to_another_origin():
    with pytest.raises(ContractError):
        next_request({'links':[{'rel':'next','href':'https://other.invalid/page'}]},[{}],
                     'https://api.example/page',{}, {'pagination':'links','url':'https://api.example/page'})


def test_resume_reuses_saved_pages_without_network():
    cfg={'url':'https://api.example','params':{'pagina':1},'pagination':'empty_page','page_param':'pagina','max_pages':3}
    visited=[]
    def load(page,key):
        visited.append(page)
        return 200,'application/json',json.dumps([{'id':1}] if page==1 else []).encode()
    result=extract(cfg,{},load,lambda *args:pytest.fail('Cached page should not be fetched'))
    assert len(result)==1 and visited==[1,2]


def test_repeated_pages_and_cap_are_failures():
    cfg={'url':'https://api.example','params':{'pagina':1},'pagination':'empty_page','page_param':'pagina','max_pages':3}
    with pytest.raises(ContractError,match='Repeated data'):
        extract(cfg,{},lambda *args:(200,'application/json',b'[{"id":1}]'),lambda *args:None)
    cfg['max_pages']=1
    with pytest.raises(ContractError,match='cap reached'):
        extract(cfg,{},lambda *args:(200,'application/json',b'[{"id":1}]'),lambda *args:None)


def test_http_error_and_missing_next_are_not_complete():
    cfg={'url':'https://api.example','pagination':'single','max_pages':1}
    with pytest.raises(ContractError,match='HTTP 401'):
        extract(cfg,{},lambda *args:(401,'application/json',b'{}'),lambda *args:None)
    with pytest.raises(ContractError,match='hasMore'):
        next_request({'hasMore':True},[],cfg['url'],{},dict(cfg,pagination='links'))


def test_declared_legacy_encoding_preserves_portuguese():
    cfg={'url':'https://api.example','pagination':'single','max_pages':1}
    body=json.dumps([{'name':'São Paulo'}],ensure_ascii=False).encode('iso-8859-1')
    rows=extract(cfg,{},lambda *args:(200,'application/json;charset=ISO-8859-1',body),lambda *args:None)
    assert rows[0][2]['name']=='São Paulo'


def test_json_decimal_is_not_rounded_through_binary_float():
    cfg={'url':'https://api.example','pagination':'single','max_pages':1}
    rows=extract(cfg,{},lambda *args:(200,'application/json',b'[{"value":9999999999999.123456}]'),lambda *args:None)
    assert rows[0][2]['value']==Decimal('9999999999999.123456')
