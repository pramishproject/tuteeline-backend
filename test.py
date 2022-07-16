import geonamescache

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
# print(gc.get_cities())
city = []
cityes = gc.get_cities()
for i in cityes:
    for j in i:
        if cityes[i]["countrycode"]=="NP":
            print(cityes[i]["name"])
            city.append(cityes[i])

# print(len(city))
    # break
# print countries dictionary
# for i in  countries:
#     print(i)
#     for j in countries[i]:
#         print(j ,":",countries[i][j])
#     break
# print(countries)