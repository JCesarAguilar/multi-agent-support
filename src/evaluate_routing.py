"""
Mide la precisión del orquestador (routing accuracy) con el golden dataset.

Uso:
    python -m src.evaluate_routing
"""

import json
from collections import defaultdict

from src import config
from src.agents.orchestrator import classify


def main() -> None:
    cases = json.loads(config.TEST_QUERIES_PATH.read_text(encoding="utf-8"))

    results = []
    for case in cases:
        decision = classify(case["query"])
        ok = decision.intent == case["expected_intent"]
        results.append((case, decision, ok))
        mark = "OK  " if ok else "FALLO"
        print(f"[{mark}] #{case['id']:>2} esperado={case['expected_intent']:<12} "
              f"obtenido={decision.intent:<12} conf={decision.confidence:.2f} | {case['query']}")

    # Precisión global
    correct = sum(ok for _, _, ok in results)
    print(f"\nRouting accuracy: {correct}/{len(results)} = {correct / len(results):.0%}")

    # Precisión por categoría
    by_category = defaultdict(lambda: [0, 0])  # categoría -> [aciertos, total]
    for case, _, ok in results:
        by_category[case["category"]][0] += ok
        by_category[case["category"]][1] += 1
    print("\nPor categoría:")
    for category, (hits, total) in by_category.items():
        print(f"  {category:<18} {hits}/{total}")

    # Detalle de los fallos: el reasoning explica por qué se equivocó
    failures = [(c, d) for c, d, ok in results if not ok]
    if failures:
        print("\nFallos (con el razonamiento del modelo):")
        for case, decision in failures:
            print(f"  #{case['id']} {case['query']}")
            print(f"     esperado={case['expected_intent']} obtenido={decision.intent}")
            print(f"     reasoning: {decision.reasoning}")


if __name__ == "__main__":
    main()