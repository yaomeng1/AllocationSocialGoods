function prodAdj = cartProd( mAdja, mAdjb )
% Computes the Cartesian product of two weighted graphs given by their
% sparse adjacency matrices.

if ~issparse(mAdja) 
    mAdja = sparse(mAdja); 
end
if ~issparse(mAdjb) 
    mAdjb = sparse(mAdjb); 
end

wa = sum(mAdja);
wb = sum(mAdjb);

[nodes1a,nodes2a,weightsa]=find(triu(mAdja));
[nodes1b,nodes2b,weightsb]=find(triu(mAdjb));
n = length(wa);
en = length(nodes1a);
m = length(wb);
em = length(nodes1b);

prodnodes1a = nodes1a*ones(1,m)+ones(en,1)*(0:n:(m-1)*n);
prodnodes2a = nodes2a*ones(1,m)+ones(en,1)*(0:n:(m-1)*n);
prodedgesa = weightsa*wb;

prodnodes1b = n*(nodes1b-1)*ones(1,n)+ones(em,1)*(1:n);
prodnodes2b = n*(nodes2b-1)*ones(1,n)+ones(em,1)*(1:n);
prodedgesb = weightsb*wa;


prodAdj = sparse(prodnodes1a,prodnodes2a,prodedgesa,n*m,n*m)+...
    sparse(prodnodes1b,prodnodes2b,prodedgesb,n*m,n*m);
prodAdj = max(prodAdj,prodAdj');

end

