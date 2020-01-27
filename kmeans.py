from numpy import*
from multiset import*
import random


def preprocess(news):   # Preprocessing the dataset
    for i, x in enumerate(news):
        news[i]=news[i][50:]   # removing timestamp and tweet ID
        
        # removing @
        starting_index=news[i].find('@') 
        if (starting_index!=-1):
            last_index=news[i].find(' ',starting_index)
            if(last_index==-1):
                
                last_index=news[i].find('\n',starting_index)
            if(last_index==-1):
                last_index= len(news[i])-1
            
            news[i]=news[i].replace(news[i][starting_index:last_index+1],"")

        
         # removing #
       
        news[i]=news[i].replace('#','')
#        
          # removing url
        starting_index=news[i].find('http://') 
        
        if (starting_index!=-1):
           
            last_index=news[i].find(' ',starting_index)
            if(last_index==-1):
#                
                last_index=news[i].find('\n',starting_index)
            if(last_index==-1):
                last_index= len(news[i])-1
            
            news[i]=news[i].replace(news[i][starting_index-1:last_index],"")

        print()
        news[i]=news[i].lower()
        
 

def calculateNewClusterCentres(clusters,jaccard_distance):
    new_cluster_centre_index=[]
    for i in clusters:
        similar_tweet_index=0
        similar_tweet_avg_distance=99999999 # setting it to big no so that it will be replaced by the avg distance of first point in cluster
        for j in  i:
            avg_distance=0
            for l in i:
                avg_distance+=(jaccard_distance[j,l])
           
            avg_distance=avg_distance/len(i)
            if avg_distance<similar_tweet_avg_distance:
                similar_tweet_avg_distance=avg_distance
                similar_tweet_index=j
               
        new_cluster_centre_index.append(similar_tweet_index)
    return new_cluster_centre_index

def calculateNewClusters(index_cluster_in_news,k,jaccard_distance,news):
    clusters=[[] for i in range(k)]
    for l,m in enumerate(news):
        min_distance_cluster=index_cluster_in_news[0]   # assume the first cluster center is the nearest to the datapoint
        for p,q in enumerate(index_cluster_in_news): 
                    if p==0: 
                        continue
                 
                    if jaccard_distance[q,l]<jaccard_distance[min_distance_cluster,l]:  #calculate new cluster center for the datapoint
                        min_distance_cluster=q
                      
        clusters[index_cluster_in_news.index(min_distance_cluster)].append(l)
    return clusters

def calculateSSE(jaccard_distance, cluster_centers,clusters):
    sse=0;
    
        
    for i,j in enumerate(clusters):
         for k in j:
            
            sse+=((jaccard_distance[cluster_centers[i],k])**2)
           
            
    return sse; 
    

def main():
    f = open('foxnewshealth.txt', 'r')
    news = f.readlines()
    f.close()
   
    preprocess(news)
    k=int(input('Enter the number of clusters'))
    initial_cluster_centers= random.sample(news,k)  # Randomly select k cluster centers from the dataset
    
    jaccard_distance= zeros((len(news),len(news)))
    print("Jaccard Distance Shape :", jaccard_distance.shape)
    index_cluster_in_news=[]
    
    clusters=[[] for i in range(k)]
    for i in range(k):
            index_cluster_in_news.append(news.index(initial_cluster_centers[i]))
   
    
    for i,j in enumerate(news):
        for l,m in enumerate(news):
            
            if j is m:
                jaccard_distance[i,l]=0
            else:
                jaccard_distance[i,l]=1-(len(Multiset(j.split(' '))&Multiset(m.split(' ')))
                /len(Multiset(j.split(' '))|Multiset(m.split(' '))))
             
    
              
    print(jaccard_distance)
    clusters= calculateNewClusters(index_cluster_in_news,k,jaccard_distance,news)
    
    
    new_cluster_centre_index=calculateNewClusterCentres(clusters,jaccard_distance)
    print()
   
    while(new_cluster_centre_index!=index_cluster_in_news):
        index_cluster_in_news=new_cluster_centre_index
        clusters= calculateNewClusters(new_cluster_centre_index,k,jaccard_distance,news)
        
        new_cluster_centre_index=calculateNewClusterCentres(clusters,jaccard_distance)
       
   
    
    print("final cluster Centers: ",)
    print()
    for m in new_cluster_centre_index:
        print(news[m])
    
    print('Cluster Number No of tweets' )
    print()
    
    for i,j in enumerate(clusters):
        print(i,'          ',len(j))
    
    print('SSE for all the clusters is ',calculateSSE(jaccard_distance,new_cluster_centre_index,clusters))
    

if __name__ == "__main__":
    main()