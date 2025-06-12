import io
import csv
import zipfile
from datetime import datetime
from flask import send_file

class ExportService:
    def gerar_csvs(self, suspeitos, mensagens):
        output = io.BytesIO()
        with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
            suspeito_csv = io.StringIO()
            writer1 = csv.writer(suspeito_csv)
            writer1.writerow(["ID", "Nome", "Apelido", "Numeros"])
            for s in suspeitos:
                numeros = [ns.numero.numero for ns in s.numerosuspeito if ns.numero]
                writer1.writerow([
                    s.id, s.nome, s.apelido, ";".join(numeros)
                ])

            zipf.writestr("suspeitos.csv", suspeito_csv.getvalue())

            mensagem_csv = io.StringIO()
            writer2 = csv.writer(mensagem_csv)
            writer2.writerow(["ID", "Remetente", "Destinatario", "Tipo", "DataHora"])

            for m in mensagens:
                writer2.writerow([
                    m.get("id", ""),
                    m.get("remetente", ""),
                    m.get("destinatario", ""),
                    m.get("tipoMensagem", ""),
                    str(m.get("timestamp", ""))
                ])

            zipf.writestr("mensagens.csv", mensagem_csv.getvalue())

        output.seek(0)
        filename = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        return send_file(output, mimetype="application/zip", as_attachment=True, download_name=filename)