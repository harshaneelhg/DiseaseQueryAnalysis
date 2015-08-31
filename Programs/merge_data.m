cd('../Data/Baidu')
load('baidu_medical.mat')
adj_matrix = [sparse(1000000,1000000,0),adj_user_query,sparse(1000000,500,0);transpose(adj_user_query),sparse(716000,716000,0),adj_query_disease;sparse(500,1000000,0),transpose(adj_query_disease),sparse(500,500,0)];
save adj_matrix