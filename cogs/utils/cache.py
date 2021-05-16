from colorama import Fore,init,Style
from functools import lru_cache
init(autoreset=True)

@lru_cache(maxsize=None)
async def cache(bot):
    #============ Color cache ============#
    try:
        bot.emb_colors = []
        QUERY = open("database/cacher.sql",'r').read()
        results = await bot.testdb1.fetch(QUERY)
        # results = await bot.db.fetch(QUERY)
        for r in results:
            bot.emb_colors.append(r["color"])
        print(Fore.YELLOW + f"[CACHE] Colors loaded!")
    except:
        print(Fore.RED + f"[CACHE] Unable to load colors!")

    #=======================================#