import argparse
from datetime import datetime
import json

parser = argparse.ArgumentParser(
    description='Updates information from the contas contained in the txt file.')
parser.add_argument('-s', '--source', dest='source',
                    help='Input file', required=True)
parser.add_argument('-v', '--data_vencimento', help='New Vencimento',
                    default=datetime.now().strftime('%Y%m%d'))

if __name__ == '__main__':
    now = datetime.now()
    num_doc_ini = int(now.timestamp())
    args = parser.parse_args()
    contas_a_pagar = []
    with open(args.source, 'r') as file:
        contas = json.load(file)
        for conta in contas['contas_a_pagar']:
            conta['num_doc_origem'] = num_doc_ini
            if conta.get('data_pagamento') == conta['data_vencimento']:
                conta['data_pagamento'] = args.data_vencimento
            conta['data_vencimento'] = args.data_vencimento
            num_doc_ini = num_doc_ini + 1
            contas_a_pagar.append(conta)

    result = json.dumps({'contas_a_pagar': contas_a_pagar},
                        indent=2, separators=(',', ': '))
    print(result)

    with open(args.source, 'w') as file:
        file.write(result)
