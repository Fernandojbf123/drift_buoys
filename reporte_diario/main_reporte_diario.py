import argparse

from reporte_diario.services.revisar_anomalias import revisar_anomalias


def main():
    parser = argparse.ArgumentParser(description="Revisar anomalías en los datos de las boyas.")
    parser.add_argument(
        "--dias", type=int, default=1, help="Número de días para revisar anomalías."
    )
    args = parser.parse_args()
    revisar_anomalias(args.dias)
    
    
    
if __name__ == "__main__":
    # Si se ejecuta directamente este script, se obtienen los valores de configuración y se llama a la función revisar_anomalias
    main()