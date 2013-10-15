import urllib

site_ls={}

def rank(links,followers,friends,favorite,total,time):
	if total==0 or followers==0:
		sig=0
	else:
		if friends==0:
			friends=1
		elif favorite==0:
			favorite=1
	sig=float(followers)/float(friends)*float(favorite)/float(total)
	links=links[0].encode('utf8')
	t=time.encode('utf8')
	return [links,t,sig]
	
def sort(ls):
    if not ls:
        return []
    else:
        pivot = ls[0]
        less = [x for x in ls[1:] if x[2] <  pivot[2]]
        greater = [x for x in ls[1:] if x[2] >= pivot[2]]
        return sort(greater) + [pivot] + sort(less)
        
def d_ls(ls):
	new_ls=[]
	for t,d,s in ls.values():
		new_ls.append([t,d,s])
	return new_ls
	
	
def check(lst):
	for ls in lst:
		if ls[0] not in site_ls:
			site_ls[ls[0]]=ls
		else:
			if ls[2]>site_ls[ls[0]][2]:
				site_ls[ls[0]]=ls 
	return d_ls(site_ls)
	#return site_ls



