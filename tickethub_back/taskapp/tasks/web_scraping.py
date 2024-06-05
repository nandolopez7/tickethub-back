# Celery
from celery import shared_task


from tickethub_back.utils.logic.web_scraping import WebScraping


@shared_task(name='ejecucion_automatica_web_scraping', autoretry_for=(Exception,), retry_kwargs={'max_retries': 1})
def ejecucion_automatica_web_scraping():
   
    # Web Scraping
    scraping = WebScraping()
    resultado = scraping.latiquetera()

    return f'Total de nuevos eventos creados: {len(resultado)}'
