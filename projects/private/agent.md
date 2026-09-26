---
title: AI-Arbeitsanweisungen
description: Verbindliche, kompakte Regeln für KI-gestützte Arbeit im privaten Repository.
type: instructions
status: active
language: de
owner: AWA
created: 2026-09-14
updated: 2026-09-16
---

# AI-Arbeitsanweisungen

## Initialisierung

Vor jeder Arbeit: `agent.md` → `index.md` → nur relevante referenzierte Dateien. Bestehende Projektdateien sind für dokumentierte Entscheidungen die Quelle der Wahrheit; explizite Nutzeranweisungen haben Vorrang.

## Sprache

- Entwicklungs-, Dokumentations- und Arbeitssprache: **Deutsch**.
- Code-Bezeichner/technische Begriffe dürfen Englisch bleiben, wenn technisch üblich oder projektkonsistent.
- Andere Sprache nur auf ausdrückliche Anweisung oder wenn das Zielformat sie erfordert.

## Schreibstil

- **Kompakt, präzise, informationsdicht.**
- Keine Fülltexte, Wiederholungen oder künstlich langen Erklärungen.
- Bestehende Terminologie und Struktur erhalten.
- Fakten, Annahmen, offene Punkte und interne Überlegungen klar trennen.
- Arbeitsdokumente so schreiben, dass sie direkt weiterbearbeitet werden können.

## Metadaten – jede Datei

Jede neu erstellte **oder inhaltlich bearbeitete Datei** benötigt Metadaten. Markdown/Text bevorzugt YAML-Frontmatter:

```yaml
---
title: Eindeutiger Titel
description: Kurzer Zweck/Inhalt
type: document
status: draft
language: de
owner: AWA
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Pflicht: `title`, `description`, `type`, `status`, `language`, `owner`, `created`, `updated`.

- Status: `draft | active | review | archived`.
- `created` nie verändern; `updated` bei materieller Änderung aktualisieren.
- Quellcode: kompakter sprachüblicher Metadaten-Header, sofern technisch zulässig.
- Formate ohne sichere Inline-Metadaten (z. B. JSON/Binär): `<dateiname>.meta.yaml`.
- Bestehende Datei ohne Metadaten: bei nächster inhaltlicher Bearbeitung ergänzen.
- Metadaten bleiben kurz; keine Fachinhalte darin duplizieren.

## Dateiregister

`index.md` ist Registry/Projektkarte.

Bei relevanter Datei-Erstellung, Verschiebung, Umbenennung, Archivierung oder Löschung `index.md` **im selben Arbeitsvorgang** aktualisieren. Eintrag kompakt: Pfad, Typ, Status, Zweck, Aktualisierungsdatum. Fachdetails bleiben in der jeweiligen Datei.

## Bearbeitung

- Bestehende Struktur erweitern; keine redundanten Parallelablagen.
- Semantisch ändern, keine blinden globalen Ersetzungen.
- Unverwandte Inhalte/Nutzeränderungen bewahren.
- Dokumentierte Entscheidungen nicht stillschweigend überschreiben.
- Arbeitsdateien dürfen Entwurf/Annahmen enthalten; diese eindeutig kennzeichnen.
- Vor Abschluss prüfen: Inhalt, Pfad, Metadaten, Registry und interne Konsistenz.

## GitHub

- Standard: `main`.
- Zusammengehörige Änderungen möglichst atomar committen.
- Vor Schreiben aktuellen Stand lesen.
- Nach Commit Pfade und Inhalt verifizieren.
- Kein Force-Push; keine neueren Änderungen überschreiben.
