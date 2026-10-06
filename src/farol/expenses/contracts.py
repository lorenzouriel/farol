"""Explicit source semantics. Unknown financial fields never become zero."""
import hashlib
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation


class ContractError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def money(value, brazilian=False):
    if value is None or isinstance(value, bool):
        raise ContractError("Missing or boolean financial value")
    text = str(value).strip()
    if brazilian:
        if not isinstance(value, str) or not re.fullmatch(r'[+-]?(?:\d+|\d{1,3}(?:\.\d{3})+)(?:,\d{1,6})?', text):
            raise ContractError('Expected Brazilian-formatted monetary string')
        text = text.replace('.', '').replace(',', '.')
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ContractError("Invalid decimal financial value") from None
    if not number.is_finite() or abs(number) >= Decimal('100000000000000') or number.as_tuple().exponent < -6:
        raise ContractError("Financial value exceeds DECIMAL(20,6)")
    return format(number, 'f')


def required(row, *keys):
    if any(k not in row or row[k] is None for k in keys):
        raise ContractError('Required fields missing: ' + ', '.join(keys))


def normalize(row, cfg):
    kind = cfg['kind']
    base = {'entity': cfg.get('entity'), 'year': cfg.get('year'), 'month': cfg.get('month'),
            'basis': None, 'currency': 'BRL'}
    if kind == 'lookup':
        return {}  # Raw directory is retained; no financial projection.
    if kind == 'cgu_funcional':
        required(row,'ano','codigoFuncao','codigoSubfuncao','codigoPrograma','codigoAcao','empenhado','liquidado','pago')
        if int(row['ano'])!=cfg['year'] or row['codigoFuncao']!=cfg['params']['funcao'] or row['codigoAcao']!=cfg['params']['acao']:
            raise ContractError('Functional expense outside configured scope')
        return dict(base,function=row['codigoFuncao'],subfunction=row['codigoSubfuncao'],program=row['codigoPrograma'],action=row['codigoAcao'],
                    basis='annual_snapshot',committed=money(row['empenhado'],True),liquidated=money(row['liquidado'],True),paid=money(row['pago'],True))
    if kind == 'cgu_emenda':
        required(row,'codigoEmenda','ano','valorEmpenhado','valorLiquidado','valorPago','valorRestoInscrito','valorRestoCancelado','valorRestoPago')
        if str(row['codigoEmenda'])!=cfg['params']['codigoEmenda'] or int(row['ano'])!=cfg['year']:
            raise ContractError('Amendment outside configured scope')
        return dict(base,amendment=str(row['codigoEmenda']),author=row.get('nomeAutor'),locality=row.get('localidadeDoGasto'),
                    basis='amendment_snapshot',committed=money(row['valorEmpenhado'],True),liquidated=money(row['valorLiquidado'],True),paid=money(row['valorPago'],True),
                    rp_registered=money(row['valorRestoInscrito'],True),rp_cancelled=money(row['valorRestoCancelado'],True),rp_paid=money(row['valorRestoPago'],True))
    if kind == 'contrato_empenho':
        required(row,'id','numero','data_emissao','empenhado','liquidado','pago','rpinscrito','rppago')
        return dict(base,document=str(row['id']),document_number=row['numero'],date=row['data_emissao'],
                    basis='linked_commitment_snapshot',committed=money(row['empenhado'],True),liquidated=money(row['liquidado'],True),paid=money(row['pago'],True),
                    rp_registered=money(row['rpinscrito'],True),rp_paid=money(row['rppago'],True))
    if kind == 'contrato_fatura':
        required(row,'id','contrato_id','emissao','valor','valorliquido','nota_cancelada')
        if str(row['contrato_id'])!=cfg['entity']:
            raise ContractError('Invoice belongs to another contract')
        return dict(base,document=str(row['id']),date=row['emissao'],basis='invoice_not_payment',
                    gross=money(row['valor'],True),net=money(row['valorliquido'],True),cancelled=row['nota_cancelada'],status=row.get('situacao'))
    if kind == 'cgu_orgao':
        required(row, 'ano', 'codigoOrgao', 'codigoOrgaoSuperior', 'orgao', 'empenhado', 'liquidado', 'pago')
        if int(row['ano']) != cfg['year'] or str(row['codigoOrgaoSuperior']) != cfg['params']['orgaoSuperior']:
            raise ContractError('CGU response outside requested organization/year')
        return dict(base, entity=str(row['codigoOrgao']), entity_name=row['orgao'],
                    superior=str(row['codigoOrgaoSuperior']), basis='annual_snapshot',
                    committed=money(row['empenhado'], True), liquidated=money(row['liquidado'], True), paid=money(row['pago'], True))
    if kind == 'tce_sp':
        required(row, 'orgao', 'evento', 'nr_empenho', 'dt_emissao_despesa', 'vl_despesa')
        date = datetime.strptime(row['dt_emissao_despesa'], '%d/%m/%Y').date()
        if date.year != cfg['year'] or date.month != cfg['month']:
            raise ContractError('TCE-SP response outside requested month')
        stages = {'Empenhado':'committed', 'Valor Liquidado':'liquidated', 'Valor Pago':'paid', 'Anulação':'cancellation_unspecified'}
        if row['evento'] not in stages:
            raise ContractError('Unmapped TCE-SP expense event')
        # Keep duplicate-looking source rows: the payload has no unique transaction ID.
        # Publish whole partition snapshots with row ordinals, never deduplicate by amount.
        return dict(base, entity_name=row['orgao'], date=date.isoformat(), document=row['nr_empenho'],
                    stage=stages[row['evento']], basis='source_movement', amount=money(row['vl_despesa'], True))
    if kind == 'ceap':
        required(row, 'ano', 'mes', 'codDocumento', 'valorDocumento', 'valorGlosa', 'valorLiquido')
        if int(row['ano']) != cfg['year'] or int(row['mes']) != cfg['month']:
            raise ContractError('CEAP response outside requested month')
        return dict(base, document=str(row['codDocumento']), basis='reimbursement',
                    gross=money(row['valorDocumento']), deductions=money(row['valorGlosa']),
                    reimbursed=money(row['valorLiquido']), category=row.get('tipoDespesa'))
    if kind in ('rreo','rgf','dca'):
        required(row, 'exercicio', 'cod_ibge', 'anexo', 'coluna', 'cod_conta', 'valor')
        if int(row['exercicio']) != cfg['year'] or str(row['cod_ibge']) != cfg['entity']:
            raise ContractError('SICONFI response outside requested scope')
        if kind != 'dca':
            required(row,'periodo','periodicidade')
            if int(row['periodo'])!=cfg['period']:
                raise ContractError('SICONFI response outside requested period')
        # Keep separate measure bases; never combine an annual statement with movements.
        if kind == 'rreo':
            if row['anexo'] != 'RREO-Anexo 01' or not row['coluna'].startswith('DESPESAS '):
                return None
            basis = 'period_movement' if 'NO BIMESTRE' in row['coluna'] else 'cumulative_statement'
        elif kind == 'rgf':
            required(row,'co_poder')
            if row['co_poder']!='E' or row['periodicidade']!='Q':
                raise ContractError('RGF power or periodicity outside requested scope')
            if row['anexo']!='RGF-Anexo 01' or not row['cod_conta'].startswith('Despesa') or row['coluna']!='TOTAL (ÚLTIMOS 12 MESES) (a)':
                return None
            basis = 'rolling_12_months'
        else:
            if row['anexo']!='DCA-Anexo I-D' or not row['coluna'].startswith('Despesas '):
                return None
            basis = 'annual_statement'
        return dict(base, statement=kind.upper(),period=row.get('periodo'),periodicity=row.get('periodicidade','A'),
                    annex=row['anexo'],account=row['cod_conta'],label=row.get('rotulo'),
                    account_name=row.get('conta'), column=row['coluna'], amount=money(row['valor']),
                    basis=basis)
    if kind == 'tce_pi_totais':
        required(row, 'exercicio', 'empenhada', 'liquidada', 'paga')
        # Upstream ignores the year parameter; filter explicitly and retain raw years.
        if int(row['exercicio']) != cfg['year']:
            return None
        return dict(base, basis='annual_snapshot', committed=money(row['empenhada']),
                    liquidated=money(row['liquidada']), paid=money(row['paga']))
    if kind == 'indicador':
        required(row, 'ANO', 'CD_ORGAO', 'NOME', 'CD_RECEBIMENTO', 'VL_DESPESA', 'VL_RECEITA', 'INDICE')
        if int(row['ANO']) != cfg['year']:
            raise ContractError('RS indicator outside requested year')
        return dict(base, entity=str(row['CD_ORGAO']), entity_name=row['NOME'], revision=str(row['CD_RECEBIMENTO']),
                    indicator=cfg['indicator'], numerator=money(row['VL_DESPESA']), denominator=money(row['VL_RECEITA']),
                    percentage=money(row['INDICE']), basis='published_ratio')
    raise ContractError('Financial contract not implemented')


def validate_batch(rows, cfg):
    projected = [normalize(row, cfg) for row in rows]
    if cfg['kind'] != 'lookup' and not any(x is not None for x in projected):
        raise ContractError('No financial records for configured scope; empty coverage is unverified')
    # Snapshot grains with authoritative IDs must be unique, not silently deduplicated.
    keys = []
    for record in projected:
        if record is None:
            continue
        if cfg['kind'] in ('cgu_orgao', 'tce_pi_totais'):
            keys.append((record['entity'], record['year']))
        elif cfg['kind'] == 'indicador':
            keys.append((record['entity'], record['year'], record['revision']))
        elif cfg['kind'] in ('rreo','rgf','dca'):
            keys.append((record['entity'], record['period'], record['annex'], record['account'], record['column'],record['label']))
        elif cfg['kind'] == 'cgu_funcional':
            keys.append((record['year'],record['function'],record['subfunction'],record['program'],record['action']))
        elif cfg['kind'] == 'cgu_emenda':
            keys.append((record['amendment'],record['locality']))
        elif cfg['kind'] in ('contrato_empenho','contrato_fatura'):
            keys.append((record['entity'],record['document']))
    if len(keys) != len(set(keys)):
        raise ContractError('Duplicate records at declared financial grain')
    return projected
