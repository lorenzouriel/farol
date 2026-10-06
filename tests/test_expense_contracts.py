from decimal import Decimal
import pytest
from farol.expenses.contracts import ContractError, money, normalize, validate_batch


def test_decimal_sign_precision_and_missing_values():
    assert money('-1.234,56',True) == '-1234.56'
    assert money('26.788') == '26.788'
    for invalid in [None,True,'NaN','Infinity','oops','0.0000001']:
        with pytest.raises(ContractError): money(invalid)
    for invalid in [123.45, '123.45', '1.23,45']:
        with pytest.raises(ContractError): money(invalid,True)


def test_cgu_scope_and_duplicate_key_block_publication():
    cfg={'kind':'cgu_orgao','year':2025,'params':{'orgaoSuperior':'26000'}}
    row=dict(ano=2025,codigoOrgao='26298',codigoOrgaoSuperior='26000',orgao='FNDE',empenhado='100,00',liquidado='80,00',pago='70,00')
    assert normalize(row,cfg)['paid']=='70.00'
    with pytest.raises(ContractError): validate_batch([row,row],cfg)
    with pytest.raises(ContractError): normalize(dict(row,ano=2024),cfg)


def test_sp_does_not_collapse_repeated_transactions_or_infer_cancellation_sign():
    cfg={'kind':'tce_sp','year':2025,'month':1,'entity':'adamantina'}
    row=dict(orgao='PM',evento='Anulação',nr_empenho='1',dt_emissao_despesa='02/01/2025',vl_despesa='10,00')
    result=validate_batch([row,row],cfg)
    assert len(result)==2
    assert result[0]['amount']=='10.00'
    assert result[0]['stage']=='cancellation_unspecified'


def test_rreo_revenue_excluded_and_measure_basis_retained():
    cfg={'kind':'rreo','year':2025,'period':1,'entity':'3550308'}
    row=dict(exercicio=2025,periodo=1,periodicidade='B',cod_ibge=3550308,anexo='RREO-Anexo 01',coluna='PREVISÃO INICIAL',cod_conta='Receita',valor=100)
    assert normalize(row,cfg) is None
    row.update(coluna='DESPESAS EMPENHADAS NO BIMESTRE',cod_conta='Despesas')
    assert normalize(row,cfg)['basis']=='period_movement'


def test_empty_financial_response_is_not_zero_spending():
    with pytest.raises(ContractError): validate_batch([],{'kind':'ceap'})


def test_pi_ignores_unrequested_years_explicitly():
    cfg={'kind':'tce_pi_totais','year':2025,'entity':'1473'}
    row=dict(exercicio=2010,empenhada=1,liquidada=1,paga=1)
    with pytest.raises(ContractError): validate_batch([row],cfg)


def test_rs_retains_published_precision():
    row=dict(ANO=2025,CD_ORGAO=1,NOME='PM',CD_RECEBIMENTO=2,VL_DESPESA=1.123,VL_RECEITA=3,INDICE=37.433)
    result=normalize(row,{'kind':'indicador','year':2025,'indicator':'MDE'})
    assert Decimal(result['numerator']) == Decimal('1.123')


def test_invoice_does_not_create_payment_measure_and_checks_contract():
    row=dict(id=1,contrato_id=474056,emissao='2025-01-01',valor='100,00',valorliquido='90,00',nota_cancelada='Não')
    cfg={'kind':'contrato_fatura','entity':'474056'}
    normalized=normalize(row,cfg)
    assert normalized['basis']=='invoice_not_payment'
    assert 'paid' not in normalized
    with pytest.raises(ContractError): normalize(row,dict(cfg,entity='other'))


def test_functional_grain_keeps_programs_separate():
    row=dict(ano=2025,codigoFuncao='12',codigoSubfuncao='123',codigoPrograma='5013',codigoAcao='20RZ',empenhado='0,00',liquidado='0,00',pago='0,00')
    cfg={'kind':'cgu_funcional','year':2025,'params':{'funcao':'12','acao':'20RZ'}}
    assert len(validate_batch([row,dict(row,codigoPrograma='5113')],cfg))==2
    with pytest.raises(ContractError): validate_batch([row,row],cfg)


def test_fiscal_rolling_and_annual_basis_are_distinct():
    row=dict(exercicio=2025,periodo=1,periodicidade='Q',co_poder='E',cod_ibge=3550308,anexo='RGF-Anexo 01',coluna='TOTAL (ÚLTIMOS 12 MESES) (a)',cod_conta='DespesaComPessoalBruta',valor=100)
    cfg={'kind':'rgf','year':2025,'period':1,'entity':'3550308'}
    assert normalize(row,cfg)['basis']=='rolling_12_months'
    assert normalize(dict(row,coluna='% sobre a RCL Ajustada'),cfg) is None
    cfg['kind']='dca'
    assert normalize(dict(row,anexo='DCA-Anexo I-D',coluna='Despesas Pagas'),cfg)['basis']=='annual_statement'
