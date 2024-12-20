import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 --> 384-dimensional embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

requirements = [
"We guarantee breakfast delivery in less than 25 minutes to all parts of the city.",
"We offer a number of prepackaged breakfasts like the mini-breakfast (one croissant, one coffee), the luxury breakfast (one croissant, one glass of orange juice, two kinds of jam, ham and eggs, one cup of coffee) and many more.",
"Of course, our customers can also assemble an individual breakfast to their taste by choosing from a long list of simple products (croissant, orange juice, butter, …). ",
"A prepackaged product may contain simple products, but also other prepackaged products.",
"So, a typical order consists of various amounts of various products (prepackaged ones and/or simple ones). ",
"Each product has a unit (e.g. 100 grams) and a price per unit denominated in Euros.",
"Currently, our customers can place orders only over the phone. To do so, they call our company number 384 29 734 and tell us their customer number.",
"A customer number has seven digits that are preceded by a two-digit area code and followed by a one digit checksum.",
"There are no collective orders of several customers.",
"After the phone clerk has authenticated the customer (which includes checking that he is not blacklisted e.g. due to bad payment morale) the customer names one or several products to be added to the shopping cart.",
"If the customer is not sure about certain products, she can tell the phone clerk the desired characteristics (e.g. less than 300 calories and less than € 4) and gets a choice of suitable products to pick from.",
"The customer can also decide to simply place a follow-up-order by naming one of her previous orders, which serves as a blueprint for the new order.",
"Those three methods of assembling the shopping cart (direct naming of products, choosing from a list of suitable products presented by the phone clerk, naming an order as a blueprint) can be combined within placing one order.",
"However, an order can only have one blueprint order at most. ",
"One order can serve as a blueprint many times.",
"For each customer, only one address is predefined. Therefore, there is no need to specify a delivery address when ordering. The process ends by the phone clerk informing the customer about the order number, which is an eight-digit number with a checksum.",
"A packing clerk looks at each order, assembles the ordered products and puts them into a paper bag. ",
"Using an ordinary text processing system, the packing clerk prints a label with his own name, the first name of the customer, the surname of the customer, the address, the order number and the delivery clerk he assigned to the order.  ",
"The label is attached to the paper bag. ",
"Also, the packing clerk prints an invoice twice with the text processing system. ",
"The invoice shows the same data as the label plus the individual ordered products, their amounts and prices and the sum total.",
"If an invoice is printed several times, each copy gets a separate number.",
"The delivery clerk calculates the optimal itinerary, often using an ordinary spreadsheet.  This is important as many orders may be fulfilled within one itinerary. ",
"The delivery clerk prints out the optimal itinerary, takes the corresponding bags and invoices and drives to the corresponding customers. ",
"Each customer confirms delivery by signing a copy of the invoice. She keeps the other copy.",
"Each customer can inquire into the status of her order over the phone using the order number. The phone clerk then tells the customer whether the delivery clerk is already on his way or not.",
"Canceling an order is possible by calling the phone clerk and naming the order number.",
"Once the order has been assembled, canceling is not possible anymore.",
"A cancelation cannot be undone.",
"Updating of orders is not possible. If the customer wants to change an order, she has to cancel it and place a new order.",
"We want the current process to be automated (but not changed) by a web-based application. The application replaces the current ordering by phone which will be discontinued. It also replaces the text processing system used for labeling and the tools used for calculating and printing the optimal itinerary.",
"The application is supposed to support the following browsers in the following versions: ...",
"The user groups are: customers, packing clerks, delivery clerks and managers. There will be no phone clerks in the future.",
"The confirmation of the delivery by the customer should also be browser-based: The delivery clerk presents a smartphone to the customer who enters her password in a browser window to confirm the delivery.",
"The software should offer a browser-based product search function that requires no authentication. The product search also replaces having the phone clerk list suitable products.",
"In the future, customers can also order by text messages (SMS). In this case they send a defined string to our company number 384 29 734. The string looks like this: C 2339110045 W mypswd P EGG 1 P TOAST 2 P OJUICE 1. This represents an order of the customer with the customer number 2339110045 having the password mypswd. The order is for one egg, two toasts and one glass of orange juice.",
"Each product has a unique product code as shown above.",
"The string may contain any number of products but is naturally limited by the length text messages can have in general.  ",
"The system responds with a text message specifying the order number the system has assigned to the order.",
"Canceling by text message should be possible by sending a text message of the form O 261273842 to the above number. In the example, the order with the order number 261273842 is canceled.",
"We have a payment system already in place. It receives interface records for expected payments. The interface record comprises the customerNumber, the orderNumber, the amountInEuros and the expected payment date. ",
"Once the packing clerk has finished assembling an order, a record representing an expected payment for the order should be transferred to the payment system.",
"The system is supposed to print a business report for the manager every night automatically that lists the orders of a given day along with the product, the amount, the packing clerk and the delivery clerk, the customer, the customer’s address and the order number.",
]

embeddings = model.encode(requirements)
embedding_matrix = np.array(embeddings)


range_n_clusters = range(2, 10)
best_n_clusters = 2
best_silhouette_score = -1

for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(embedding_matrix)
    silhouette_avg = silhouette_score(embedding_matrix, cluster_labels)
    if silhouette_avg > best_silhouette_score:
        best_silhouette_score = silhouette_avg
        best_n_clusters = n_clusters

print(f"\nOptimal number of clusters: {best_n_clusters}\n")

kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
kmeans.fit(embedding_matrix)
cluster_labels = kmeans.labels_

clusters = {}
for idx, label in enumerate(cluster_labels):
    clusters.setdefault(label, []).append(requirements[idx])

for cluster, reqs in clusters.items():
    print(f"Cluster {cluster}:")
    for req in reqs:
        print(f"  - {req}")
    print()