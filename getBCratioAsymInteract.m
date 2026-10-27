function bcr = getBCratioAsymInteract( mAdj, varargin )
%% this function allows the interaction graph to contain isoloated nodes
% - The first parameter is the adjacent matrix of relacement graph
% - The seconde parameter is the adjacent matrix of the interaction graph
% Computes the critical b/c ratio for a graph given by weighted 
% (replacement) adjacency
% matrix mAdj. 
% A first optional argument represents a distinct interaction matrix mInt
% A second optional argument can be used to pass a precomputed matrix of
% remeeting times. This is useful for analyzing different interaction
% matrices with the same replacement matrix

n = length(mAdj);
w = sum(mAdj);
W = sum(w);
pi = (w/W)'; % column vector
if length(varargin) < 2
    Rem = findRemeetingTimes(mAdj);
else
    Rem = varargin{2};
end;
Rem = Rem - diag(diag(Rem));
if length(varargin) < 1
    mInt = mAdj;
else
    mInt = varargin{1};
end

w_I = sum(mInt,2); % column vector

% P01 = mInt./w_I; % replace the degree for isolated node with 1 and calculate qij(snap)

P10 = normalizedLaplacian(mAdj)+speye(n);

P20 = P10 * P10;
% P21 = P20 * P01';

T20 = sum(pi.*P20.*w_I'.*Rem,"all");
T21 = sum(pi.*(P20*mInt').*Rem,"all");
T01 = sum(pi.*(mInt').*Rem,"all");
bcr = T20 / (T21 - T01);
bcr =full(bcr);
end

