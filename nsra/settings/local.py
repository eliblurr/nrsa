from dotenv import load_dotenv
import os

load_dotenv()

if os.getenv('ENVIRONMENT', 'dev').lower() in ['prod']:
    from nsra.settings.production import *  

    try:

        KEY_ROOT = os.path.join(BASE_DIR, 'x64js/')
        LOG_ROOT = os.path.join(BASE_DIR, 'logs/')

        if not os.path.isdir(KEY_ROOT):os.mkdir(KEY_ROOT)
        if not os.path.isdir(LOG_ROOT):os.mkdir(LOG_ROOT)

        DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(KEY_ROOT, "private.txt")
        DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(KEY_ROOT, "public.txt")

        if not (os.path.isfile(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH) and os.path.isfile(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH)):
            os.system(f'sh keys.sh -r {KEY_ROOT}')

        with open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+") as public:
            SECRET_KEY = public.readline().strip("\n")

    except:
        pass

else:
    from nsra.settings.dev import *  

# Override settings here

