"""
Script de lancement de tous les tests avec génération de rapport.
"""

import unittest
import sys
import io
import datetime
import os

def run_tests():
    # S'assurer que le dossier de rapports existe
    if not os.path.exists("reports"):
        os.makedirs("reports")

    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")

    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=2)
    result = runner.run(suite)

    output = buffer.getvalue()
    
    # Calcul dynamique plus précis
    skipped = len(result.skipped)
    failures = len(result.failures)
    errors = len(result.errors)
    successes = result.testsRun - (failures + errors + skipped)

    summary = (
        f"\n{'='*60}\n"
        f"RÉSUMÉ\n"
        f"{'='*60}\n"
        f"Tests exécutés : {result.testsRun}\n"
        f"Succès         : {successes}\n"
        f"Échecs         : {failures}\n"
        f"Erreurs        : {errors}\n"
        f"Sauts          : {skipped}\n"
        f"Résultat       : {'OK' if result.wasSuccessful() else 'ÉCHEC'}\n"
    )

    # Affichage et sauvegarde
    now = datetime.datetime.now()
    timestamp_display = now.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = now.strftime("%Y%m%d_%H%M%S")
    
    final_report = f"Rapport de tests - {timestamp_display}\n{'='*60}\n\n{output}\n{summary}"
    
    print(final_report)

    report_path = os.path.join("reports", f"report_{timestamp_file}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(final_report)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
