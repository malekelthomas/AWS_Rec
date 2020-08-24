import requests
import json
import csv

CATEGORIES = ["games", "pc", "electronics", "shoes", "clothes", "jewelry", "headphones"]


def product_getter(user_id, keyword):

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"

    querystring = {"country":"US","keyword":keyword}

    headers = {
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com",
        'x-rapidapi-key': "b40cb29b58mshef93c5cf5e102a1p1a7b7fjsn090a508800d0"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open(user_id+"_"+keyword+"_products.json", "w") as f:
        json.dump(response.json(), f)

    print("Products found\n")

def product_generator(user_id,keyword):
    
    product_getter(keyword)

    with open(user_id+"_"+keyword+"_products.json", "r") as f:
        data = json.load(f)
        count = 0
        for product in data['products']:
            if product['reviews'] < 300:
                print("Wtf", product['title'],"\n")
                continue
            if count == 5:
                break
            else:
                print(product['title']+"\n")
            count+=1
        data.close()



def category_chooser_rater():

    ratings_dict = {}
    with open("categories.json", "r") as f:
        categories = json.load(f)
        for category in categories["Categories"]:
            for related in category:
                ratings_dict[related] = 0
                print(related, end=" ")
    
        print("\n")
        print(ratings_dict)
        print("-----------------------------------")

        user_in = input("Choose a category: ").strip()
        ratings_dict[user_in]+=1
        print(ratings_dict)

        for category in categories["Categories"]:
            for related in category:
                if user_in != related:
                    break
                for i in category[related]:
                    if related == 'Games' or related == 'Clothes':
                        print(i,related)
                    else:
                        if type(i) == dict:
                            for j in i:
                                for other_categories in i[j]:
                                    print(other_categories)
                                    break
                        else:
                            print(i)
        user_in2 = input("Interested in any of these?: ")
        ratings_dict[user_in]+=1
        ratings_dict[user_in2]=1
        print(ratings_dict)
    
    with open("ratings.csv", "w") as f:
        f.write("Category,Clicks\n")
        for key in ratings_dict.keys():
            f.write("{},{}\n".format(key, ratings_dict[key]))

    


category_chooser_rater()