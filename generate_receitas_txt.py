import argparse
from datetime import datetime
import json
import random
import os

today = datetime.now()

parser = argparse.ArgumentParser(
    description="Generate a set of contas_a_pagar records that can be later imported in dootax"
)

parser.add_argument(
    "-o",
    "--output",
    dest="destination",
    default="/Users/jorgecorradi/Desktop",
    help="Where the file should be generated. Default: /Users/jorgecorradi/Desktop",
)
parser.add_argument(
    "-q",
    "--quantity",
    dest="quantity",
    help="Quantity of records to be generated",
    default=1,
    type=int,
)
parser.add_argument(
    "-e", "--cod_empresa", dest="cod_empresa", help="Company code", required=True
)
parser.add_argument("-s", "--cod_estab", dest="cod_estab", default="0001")
parser.add_argument(
    "-a", "--cod_arrecadacao", dest="cod_arrecadacao", default="0001", required=True
)
parser.add_argument(
    "-r", "--cod_receita", dest="cod_receita", help="Revenue code", required=True
)
parser.add_argument(
    "-d", "--det_receita", dest="det_receita", help="Revenue detail code"
)
parser.add_argument("--uf", dest="uf", help="UF favorecida", required=True)
parser.add_argument(
    "-b",
    "--vlr_base_calc",
    dest="vlr_base_calc",
    help="Valor da base de cálculo",
    default=0,
)
parser.add_argument("-p", "--periodo", dest="periodo", required=False)
parser.add_argument(
    "-v",
    "--data_vencimento",
    dest="data_vencimento",
    help="Due Date",
    default=today.strftime("%Y%m%d"),
)
parser.add_argument(
    "-g",
    "--data_pagamento",
    dest="data_pagamento",
    help="Due Date",
    default=today.strftime("%Y%m%d"),
)
parser.add_argument(
    "-c",
    "--console",
    help="If true, will show it instead of generating file",
    action="store_true",
)


def get_first_day_of_last_month(date_as_string):
    d = datetime.strptime(date_as_string, "%Y%m%d")
    d.replace(
        year=d.year if d.month > 1 else d.year - 1,
        month=d.month - 1 if d.month > 1 else 12,
        day=1,
    )
    return d.strftime("%Y%m%d")


if __name__ == "__main__":
    args = parser.parse_args()
    now = datetime.now()
    num_doc_ini = int(now.timestamp())

    contas_a_pagar = []
    for i in range(0, args.quantity):
        conta = {}
        conta["cod_empresa"] = args.cod_empresa
        conta["cod_estab"] = args.cod_estab
        conta["data_vencimento"] = args.data_vencimento
        conta["data_pagamento"] = args.data_pagamento
        conta["cod_arrecadacao"] = args.cod_arrecadacao
        conta["cod_receita"] = args.cod_receita
        conta["uf_favorecida"] = args.uf
        if args.det_receita is not None:
            conta["det_receita"] = args.det_receita
        if args.vlr_base_calc != 0:
            conta["vlr_base_calc"] = args.vlr_base_calc
        conta["vlr_principal"] = (
            0
            if args.vlr_base_calc != 0
            else round(random.randint(1000, 990000) / 100, 2)
        )
        conta["periodo"] = (
            args.periodo
            if args.periodo is not None
            else get_first_day_of_last_month(args.data_vencimento)
        )
        conta["num_doc_origem"] = num_doc_ini + i
        conta[
            "info_complementar"
        ] = f'Receita: {args.cod_arrecadacao} - {args.cod_receita} ({args.uf}). det: {args.det_receita if args.det_receita is not None else "-"}'

        contas_a_pagar.append(conta)

    result = json.dumps(
        {"contas_a_pagar": contas_a_pagar}, indent=2, separators=(",", ": ")
    )
    if args.console:
        print(result)
    else:
        if not os.path.exists(args.destination):
            os.makedirs(args.destination)
        with open(
            f'{args.destination}/{args.cod_empresa}-{args.cod_arrecadacao}-{args.uf}-{args.cod_receita}{"-" + args.det_receita if args.det_receita is not None else ""}.txt',
            "w",
        ) as file:
            file.write(result)
            print(f"File generated: {file.name}")
