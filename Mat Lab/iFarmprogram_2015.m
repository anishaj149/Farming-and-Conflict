clear;
%%where the data is located
dir = '/Users/anisha/Documents/iFARM/';

%%load data
load([dir 'iFarmData(2015)_1_28_2019.mat']);
%NC_Bou(170) = NaN;
%reNC_Bou = reshape(NC_Bou, [170 1]);
%chk_NC = load('O:\lisk\shareBetweenWorkstations\NC_Bou.mat');
%reChk_NC = reshape(chk_NC.NC_Bou, [170 1]);
%chk_NC2 = load('C:\Users\mlisk\Google Drive\Zhang_Lab_Data\GlobalAgricultureModel\Results\Nbudget_11-Jul-2018.mat');
%reChk_NC2 = reshape(chk_NC2.contentN, [170 1]);
%chk_NC3 = load('C:\Users\mlisk\Google Drive\Zhang_Lab_Data\GlobalAgricultureModel\Results\Result_20151016.mat');
%reChk_NC3 = reshape(chk_NC2.contentN, [170 1]);



%%Guided Solution 3.2
%%a. - One Country, One Crop, One Year
%%first, save several important indicies used in the following analyses to
%%variables for easy access during the analyses
chaInd = find(ismember(FAOSTAT_CoName_FAO,'China'));
riceInd = find(ismember(FAOSTAT_CrName_FAO,'Rice; paddy'));
yr1986 = find(Yr==1986);
yr2010 = find(Yr==2010);
yr2011 = find(Yr==2011);
yr2015 = find(Yr==2015);
numCos = length(FAOSTAT_CoName_FAO);
numCrops = length(FAOSTAT_CrName_FAO);
numTrdYrs = length(yr1986:yr2015);

%%N inputs
chaRiceNIn2010 = nansum([Nfer_kgkm(chaInd,riceInd,yr2010), Nman_kgkm(chaInd,riceInd,yr2010),...
                        Nfix_kgkm(chaInd,riceInd,yr2010), Ndep_kgkm(chaInd,riceInd,yr2010)]);
%%N surplus
chaRiceNSur2010 = chaRiceNIn2010 - Nyield_kgkm(chaInd,riceInd,yr2010);
%%NUE
chaRiceNUE2010 = Nyield_kgkm(chaInd,riceInd,yr2010) / chaRiceNIn2010;


%%b. - All Countries, All Crops, All Years, Aggregate by Crops
%%N Surplus
globeCropIn = Nfer_kgkm + Nman_kgkm + Nfix_kgkm + Ndep_kgkm;
globeCropSur = globeCropIn - Nyield_kgkm;
%%Aggregate the crops, N Surplus
globalCropAgg = reshape(nansum(globeCropSur.*AreaH_FAO,2) ./ nansum(AreaH_FAO,2),... 
                    [numCos length(Yr)]);
%%NUE
globalCropNUE = reshape(nansum(Nyield_kgkm.*AreaH_FAO,2) ./ nansum(globeCropIn.*AreaH_FAO,2),... 
                    [numCos length(Yr)]);


%%3.2.2 - How much N has China been importing?
%%a. - amount N in traded crops
tradeN = nan(size(netImTrade));
for i = 1:length(NC_Bou)
    tradeN(i,:,:,:) = netImTrade(i,:,:,:) * NC_Bou(i);
end

%%b - net N input to China
netNIm_China = nansum(reshape(tradeN(:,:,chaInd,:), [numCrops numTrdYrs numCos]), 3);

%%c - aggregate by crops
agNIm_China = nansum(netNIm_China, 1);


%%3.2.3 - Amount of N pollution if China did not import
%%a. amount of N surplus China would have produced without trade
chinaNUE = reshape(NUE_3d(chaInd,:,yr1986:yr2015),[numCrops numTrdYrs]);
notImN_China = ((1./chinaNUE)-1) .* netNIm_China;

%%b. aggergate by crops
agNotImN_China = nansum(notImN_China, 1);


%random arrays for prac

x = [1 2; 3 4];
y = x * x;

%years from 1986 to 2016 in net imtrade
%imports for each crop x year:
china_imports = squeeze(nansum(netImTrade(:,1:26,40,:), 4));
china_pollution = squeeze(Nexc_kgkm(40,:,26:51));
china_yield = squeeze(Yield_FAO(40,:,26:51));

% crop x year = added nitrogen pollution by china
china_added_pollution = china_imports .* china_pollution ./ china_yield;








