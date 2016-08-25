#!usr/bin/env python

import csv, random, operator, sys, math

#builds the budgets, query, opt from the csv's reader object
def build(reader):
	budgets = dict()
	query_bidders = dict()
	for row in reader:
		
		bidder, query, bid, budget = row
		bid = float(bid)
		if(budget != ""):

			budget = float(budget)
			budgets[bidder] = budget
			
		if(query not in query_bidders):
			query_bidders[query] = []
		query_bidders[query] += [(bidder, bid)]
	opt =  0
	for bidder in budgets:
		opt += budgets[bidder]
	return (budgets, query_bidders, opt)

#Calculates the revenue genreated based on the method provided
def calc(bb,queries,qb,method):
	budgets = dict(bb)
	query_bidders = dict(qb)
	rev = 0

	remaining = {}
	for b in budgets:
		remaining[b] = budgets[b]

	for query in queries:
		if(query==''):
			pass
		else:
			bidders = query_bidders[query]
			if(method=='greedy'):
				
				bidders = [x for x in bidders if remaining[x[0]] >= x[1]]
				bidders = sorted(bidders, key= lambda x: x[0])
				bidders = sorted(bidders, key= lambda x: -x[1])

			elif(method=='balance'):
				
				bidders = [x for x in bidders if remaining[x[0]] >= x[1]]
				bidders = sorted(bidders, key= lambda x: -x[1])
				bidders = sorted(bidders, key= lambda x: -remaining[x[0]])

			else:

				bidders = [x for x in bidders if remaining[x[0]] >= x[1]]
				bidders = sorted(bidders, key= lambda x: -(1-math.e**(-1*(remaining[x[0]]/budgets[x[0]]))) * x[1])

			if(len(bidders)!=0):
				max_bidder, max_bid = bidders[0]
				remaining[max_bidder] -= max_bid
				rev += max_bid
	return rev


def main():
	if(len(sys.argv) != 2):
		print "python adwords.py [greedy | mssv | balance]"
		exit(1)
	method = sys.argv[1]
	header = True
	csvfile = open('bidder_dataset.csv','rb')
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')	
	
	if(header):
		reader.next()
	
	#budget stores the budget of each bidder
	#query_bidders stores the list of all bidders that have bid for this query
	#opt is the optimal cost 
	budgets, query_bidders, opt = build(reader)
	
	qf = open("queries.txt")
	queries = qf.read().split("\n")
	total = 0 
	rounds = 100
	random.seed(0);	
	rev = 0
	for i in xrange(rounds):
		rev = calc(budgets, queries, query_bidders, method)
		total += rev
		random.shuffle(queries)
	#Calculate the compettive ratio
	cr = round(total/(rounds*opt),2);
	print total/rounds, cr

if( __name__ == '__main__'):
	main();
