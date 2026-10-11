# LarsGade.com – statisk GitHub Pages-hjemmeside

HTML, CSS og JavaScript. Ingen Cloudflare Worker, R2, database eller serverlogin.

## Aktivering

Repository Settings → Pages → Source: GitHub Actions. Workflow Publish website bygger og publicerer automatisk ved commits til main. Åbn først https://larsgade.github.io/larsgade.com/ og test. Tilføj derefter dit eget domæne i Pages-indstillingerne, og ændr DNS efter GitHubs officielle vejledning. Cloudflare kan fjernes som hosting; domænets DNS kan administreres hos din foretrukne udbyder. Bevar mailens DNS-poster.

## Administration

Åbn admin.html, eller klik tre gange hurtigt på krediteringen. Opret en GitHub fine-grained personal access token med adgang kun til LarsGade/larsgade.com og Contents: Read and write. Indtast den i admin, og klik Connect. Nøglen bruges kun i denne sides hukommelse; den gemmes ikke i repositoryet eller localStorage. En refresh kræver, at den indtastes igen. Del ikke nøglen. Admin-siden er offentlig, men GitHub kræver gyldig autorisation til at skrive ændringer.

Faner: Site status, Files, Videos, Images, Upload, Links. Save gemmer site-config.json som en commit. Workflowet starter derefter publicering, som kan tage nogle minutter. Refresh pCloud folders gemmer en genindlæsningsanmodning og starter en ny publicering. Hvis du tilføjer/fjerner filer i pCloud, skal du bruge denne knap. Mappeoversigten opdateres ikke automatisk uden en ny publicering.

Files, Videos og Images bruger pCloud Public Folder-links fra filedn.eu eller filedn.com. GitHub Actions læser mapperne rekursivt og bygger folder-index.json til hjemmesiden. Mapper og filnavne er offentlige, og siden har ingen adgangskodefelter. Native videoafspilning og Chromecast bevares; understøttelse af MKV/MPEG og codecs afhænger af browser og Chromecast. Upload bruger et pCloud-uploadlink og uploader direkte til pCloud. Links kan oprettes, redigeres, slettes og sorteres. Logoer angives som billedlinks.

Hvis mappelinket er forkert eller pCloud er utilgængelig, fejler workflowet og den tidligere udgivelse forbliver aktiv. Ret linket i admin og gem igen. GitHub afviser samtidig redigering med en konflikt, hvis site-config.json er ændret af andre; forbind igen, før du gemmer.

## Lokalt

Python 3.12+: python scripts/build.py, derefter python -m http.server 8000 --directory _site. Ingen npm-installation nødvendig. PCloud-filer, gamle admin-data og adgangskoder er ikke inkluderet. Indsæt de ønskede links i admin. Sprogknappen Dansk/English husker sprogvalget i browseren.
