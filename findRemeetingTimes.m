function remTime = findRemeetingTimes( mAdj, varargin )
% Computes remeeting times of the simple random walk on a graph
% given by its weighted adjacency matrix mAdj
if ~issparse(mAdj)
    mAdj= sparse(mAdj);
end
mAdj = max(mAdj,mAdj');
n = length(mAdj);
C = cartProd(mAdj,mAdj);
s = sum(C).'/2;
L = spdiags(sum(C).',0,length(C),length(C)) - C;
LL = normalizedLaplacian(mAdj);
diagcoords = 1:n+1:n^2;
othercoords = sparse(1:n^2);
othercoords(diagcoords)=0;
othercoords = find(othercoords);
s = s(othercoords);
L = L(othercoords,othercoords);
remTime = zeros(n);
remTime(othercoords) = L\s;
remTime=remTime+diag(diag(1+(LL*remTime+remTime*LL')/2));
end

