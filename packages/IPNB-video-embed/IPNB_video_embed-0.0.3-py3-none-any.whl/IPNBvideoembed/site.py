from ensure import ensure_annotations
from urllib import request
from IPNBvideoembed.custom_exception import InvalidURLException
from IPNBvideoembed.logger import logger
from IPython import display


@ensure_annotations
def is_valid_url(url: str) -> bool:
    try:
        status = request.urlopen(url).getcode()
        assert status == 200
        return True
    except Exception as e:
        logger.exception(e)
        return False


@ensure_annotations
def embed_site(url: str, width: str = "100%", height: int = 600) -> str:
    try:
        if is_valid_url(url):
            response = display.IFrame(src=url, width=width, height=height)
            display.display(response)
            logger.info(f"Rendered {url} successfully")
            return "success"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e
