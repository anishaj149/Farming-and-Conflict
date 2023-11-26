clear;
%%where the data is located
dir = '/Users/anisha/Documents/iFARM/';

%%load data
load([dir 'iFarmData(2015)_1_28_2019.mat']);

Africa = ["Nigeria", "Ethiopia", "Egypt", "Democratic Republic of the Congo", "South Africa", "Kenya", "Uganda", "Algeria", "Sudan (former)", "Morocco", "Angola", "Mozambique", "Ghana", "Madagascar", "Cameroon", "C?te dIvoire", "Niger", "Burkina Faso", "Mali", "Malawi", "Zambia", "Senegal", "Chad", "Somalia", "Zimbabwe", "Guinea", "Rwanda", "Benin", "Burundi", "Tunisia", "Togo", "Sierra Leone", "Libya", "Congo", "Liberia", "Central African Republic", "Mauritania", "Eritrea", "Namibia", "Gambia", "Botswana", "Gabon", "Lesotho", "Guinea-Bissau", "Equatorial Guinea", "Mauritius", "Djibouti", "Comoros", "Western Sahara", "Sao Tome and Principe", "Seychelles"];
%51
Europe = ["Russian Federation", "Germany", "United Kingdom", "France", "Italy", "Spain", "Ukraine", "Poland", "Romania", "Netherlands", "Belgium", "Czech Republic", "Greece", "Portugal", "Sweden", "Hungary", "Belarus", "Austria", "Serbia", "Switzerland", "Bulgaria", "Denmark", "Finland", "Slovakia", "Norway", "Ireland", "Croatia", "Bosnia and Herzegovina", "Albania", "Lithuania", "Slovenia", "Latvia", "Estonia", "Montenegro", "Luxembourg", "Iceland", "Liechtenstein"];
%36
NA = ["United States of America", "Mexico", "Canada"];
%3
LA = ["Guatemala", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama", "Colombia", "Venezuela (Bolivarian Republic of)", "Ecuador", "Peru", "Bolivia (Plurinational State of)", "Brazil", "French Guiana", "Paraguay", "Chile", "Argentina", "Uruguay", "Cuba", "Haiti", "Dominican Republic", "Puerto Rico", "Brazil", "Haiti", "Guyana"];
%24
Asia = ["China" "India" "Kazakhstan" "Mongolia" "Indonesia" "Pakistan" "Turkey" "Myanmar" "Afghanistan" "Yemen" "Thailand" "Turkmenistan" "Uzbekistan"	"Japan" "Viet Nam" "Malaysia" "Philippines" "Kyrgyzstan" "Cambodia" "Bangladesh" "Nepal" "Tajikistan" "Azerbaijan" "Georgia" "Bhutan" "Armenia" "Cyprus" "Singapore" "Maldives"];
%29
ME = ["Algeria", "Bahrain", "Djibouti", "Egypt", "Iran (Islamic Republic of)", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Libya", "Malta", "Morocco", "Oman", "Qatar", "Saudi Arabia", "Syrian Arab Republic", "Tunisia", "United Arab Emirates", "Yemen"];
%20
%Asia, ME, NA, LA, Africa, Euro (91-95, 96-00, 01-05, 06-10)
sentiment_avgs = [-0.03225806451612903 0.11044176706827309 -0.154 0.29568788501026694 -0.1446028513238289 0.048879837067209775 -0.184 0.29606625258799174 0.31313131313131315 0.5313131313131313 0.23217922606924643 0.725531914893617 -0.18162839248434237 0.1488469601677149 0.00819672131147541 -0.13131313131313133 -0.3216494845360825 0.036734693877551024 -0.16260162601626016 0.1748971193415638 -0.006224066390041493 0.1425661914460285 -0.07302231237322515 0.07740585774058577];

yr1986 = find(Yr==1986);
yr2011 = find(Yr==2011);
yr2015 = find(Yr==2015);
yr1991 = find(Yr==1991);
yr1995 = find(Yr==1995);
yr1996 = find(Yr==1996);
yr2000 = find(Yr==2000);
yr2001 = find(Yr==2001);
yr2005 = find(Yr==2005);
yr2006 = find(Yr==2006);
yr2010 = find(Yr==2010);
numCos = length(FAOSTAT_CoName_FAO);
numCrops = length(FAOSTAT_CrName_FAO);
numTrdYrs = length(yr1986:yr2015);

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

AfricaNUE = zeros(1, 55, 'double');
AfricaPollution = zeros(1, 55, 'double');
for n = 1: length(Africa)
    current_country = Africa(n);
    country_index = find(strcmp(FAOSTAT_CoName_FAO,current_country));
    %country_ID = FAOSTAT_CoCODE_FAO(country_index);
    country_NUE = globalCropNUE(country_index, :);
    country_NUE(isnan(country_NUE)) = 0;
    country_NUE = country_NUE .* squeeze(nansum(AreaH_FAO(country_index, :, :), 2)); 
    AfricaNUE = AfricaNUE + country_NUE;
    country_Pollution = globalCropAgg(country_index, :);
    country_Pollution(isnan(country_Pollution)) = 0;
    disp(AfricaPollution);
    AfricaPollution(1,:) = AfricaPollution + country_Pollution;
end
disp("hi");
disp(AfricaPollution);
AfricaPollution = AfricaPollution / 51;
Africa_avg_pollution = [sum(AfricaPollution(1, yr1991:yr1995))/5, sum(AfricaPollution(1, yr1996:yr2000))/5, ...
    sum(AfricaPollution(1, yr2001:yr2005))/5, sum(AfricaPollution(1, yr2006:yr2010))/5];


AsiaNUE = zeros(1, 55, 'double');
AsiaPollution = zeros(1, 55, 'double');
for n = 1: length(Asia)
    current_country = Asia(n);
    country_index = find(strcmp(FAOSTAT_CoName_FAO,current_country));
    %country_ID = FAOSTAT_CoCODE_FAO(country_index);
    country_NUE = globalCropNUE(country_index, :);
    country_NUE(isnan(country_NUE)) = 0;
    
    %country_NUE = country_NUE .* squeeze(nansum(AreaH_FAO(country_index, :, :), 2)); 
    AsiaNUE = AsiaNUE + country_NUE;
    country_Pollution = globalCropAgg(country_index, :);
    country_Pollution(isnan(country_Pollution)) = 0;
    AsiaPollution(1,:) = AsiaPollution + country_Pollution;
end
AsiaPollution = AsiaPollution/29; 
Asia_avg_pollution = [sum(AsiaPollution(1, yr1991:yr1995))/5, sum(AsiaPollution(1, yr1996:yr2000))/5, ...
    sum(AsiaPollution(1, yr2001:yr2005))/5, sum(AsiaPollution(1, yr2006:yr2010))/5];

EuroNUE = zeros(1, 55, 'double');
EuroPollution = zeros(1, 55, 'double');
for n = 1: length(Europe)
    current_country = Europe(n);
    country_index = find(strcmp(FAOSTAT_CoName_FAO,current_country));
    %country_ID = FAOSTAT_CoCODE_FAO(country_index);
    country_NUE = globalCropNUE(country_index, :);
    country_NUE(isnan(country_NUE)) = 0;
    
    %country_NUE = country_NUE .* squeeze(nansum(AreaH_FAO(country_index, :, :), 2)); 
    EuroNUE = EuroNUE + country_NUE;
    country_Pollution = globalCropAgg(country_index, :);
    country_Pollution(isnan(country_Pollution)) = 0;
    EuroPollution(1,:) = EuroPollution + country_Pollution;
end
EuroPollution = EuroPollution/ 36; 
Euro_avg_pollution = [sum(EuroPollution(1, yr1991:yr1995))/5, sum(EuroPollution(1, yr1996:yr2000))/5, ...
    sum(EuroPollution(1, yr2001:yr2005))/5, sum(EuroPollution(1, yr2006:yr2010))/5];

MENUE = zeros(1, 55, 'double');
MEPollution = zeros(1, 55, 'double');
for n = 1: length(ME)
    current_country = ME(n);
    country_index = find(strcmp(FAOSTAT_CoName_FAO,current_country));
    %country_ID = FAOSTAT_CoCODE_FAO(country_index);
    country_NUE = globalCropNUE(country_index, :);
    country_NUE(isnan(country_NUE)) = 0;
    
    %country_NUE = country_NUE .* squeeze(nansum(AreaH_FAO(country_index, :, :), 2)); 
    MENUE = MENUE + country_NUE;
    country_Pollution = globalCropAgg(country_index, :);
    country_Pollution(isnan(country_Pollution)) = 0;
    MEPollution(1,:) = MEPollution + country_Pollution;
end
MEPollution = MEPollution/20;
ME_avg_pollution = [sum(MEPollution(1, yr1991:yr1995))/5, sum(MEPollution(1, yr1996:yr2000))/5, ...
    sum(MEPollution(1, yr2001:yr2005))/5, sum(MEPollution(1, yr2006:yr2010))/5];

NANUE = zeros(1, 55, 'double');
NAPollution = zeros(1, 55, 'double');
for n = 1: length(NA)
    current_country = NA(n);
    country_index = find(strcmp(FAOSTAT_CoName_FAO,current_country));
    %country_ID = FAOSTAT_CoCODE_FAO(country_index);
    country_NUE = globalCropNUE(country_index, :);
    country_NUE(isnan(country_NUE)) = 0;
    
    %country_NUE = country_NUE .* squeeze(nansum(AreaH_FAO(country_index, :, :), 2)); 
    NANUE = NANUE + country_NUE;
    country_Pollution = globalCropAgg(country_index, :);
    country_Pollution(isnan(country_Pollution)) = 0;
    NAPollution(1,:) = NAPollution + country_Pollution;
end
NAPollution = NAPollution/3; 
NA_avg_pollution = [sum(NAPollution(1, yr1991:yr1995))/5, sum(NAPollution(1, yr1996:yr2000))/5, ...
    sum(NAPollution(1, yr2001:yr2005))/5, sum(NAPollution(1, yr2006:yr2010))/5];

LANUE = zeros(1, 55, 'double');
LAPollution = zeros(1, 55, 'double');
LALand = zeros(1, 55, 'double');
for n = 1: length(LA)
    current_country = LA(n);
    country_index = find(strcmp(FAOSTAT_CoName_FAO,current_country));
    %country_ID = FAOSTAT_CoCODE_FAO(country_index);
    country_NUE = globalCropNUE(country_index, :);
    country_NUE(isnan(country_NUE)) = 0;
    LALand = LALand + squeeze(nansum(AreaH_FAO(country_index, :, :), 2));
    %country_NUE = country_NUE .* squeeze(nansum(AreaH_FAO(country_index, :, :), 2)); 
    LANUE = LANUE + country_NUE;
    country_Pollution = globalCropAgg(country_index, :);
    country_Pollution(isnan(country_Pollution)) = 0;
    LAPollution(1,:) = LAPollution + country_Pollution;
end
LAPollution = LAPollution/24;
LA_avg_pollution = [sum(LAPollution(1, yr1991:yr1995))/5, sum(LAPollution(1, yr1996:yr2000))/5, ...
    sum(LAPollution(1, yr2001:yr2005))/5, sum(LAPollution(1, yr2006:yr2010))/5];



global_avgs = [Asia_avg_pollution ME_avg_pollution NA_avg_pollution LA_avg_pollution Africa_avg_pollution Euro_avg_pollution];

scatter(sentiment_avgs, global_avgs);
%{
x = sentiment_avgs(1, 1:4);
y = global_avgs(1, 1:4);
plot(x,y)

hold on;
x1 = sentiment_avgs(1, 5:8);
y1 = global_avgs(1, 5:8);
plot(x1,y1)

hold on;
x2 = sentiment_avgs(1, 9:12);
y2 = global_avgs(1, 9:12);
plot(x2,y2)

hold on;
x3 = sentiment_avgs(1, 13:16);
y3 = global_avgs(1, 13:16);
plot(x3,y3)

hold on;
x4 = sentiment_avgs(1, 17:20);
y4 = global_avgs(1, 17:20);
plot(x4,y4)

hold on;
x5 = sentiment_avgs(1, 21:24);
y5 = global_avgs(1, 21:24);
plot(x5,y5)
%}




coefficients = polyfit(sentiment_avgs, global_avgs, 2);
numFitPoints = 1000;  %Enough to make the plot look continuous.
xFit = linspace(min(sentiment_avgs), max(sentiment_avgs), numFitPoints);
yFit = polyval(coefficients, xFit);
hold on;
plot(xFit, yFit, 'r-', 'LineWidth', 2);
grid on;




%legend({'Asia','Middle East', 'North America', 'Latin America', 'Africa', 'Europe'},'Location','northeast','Orientation','vertical');
xlabel('Instability')
ylabel('Pollution')
title('Nitrogen Pollution Levels for Regional Conflict Measures')



disp(AsiaPollution(1, yr1991:yr1995));
disp(AsiaPollution(1, yr1996:yr2000));
disp(AsiaPollution(1, yr2001:yr2005));
disp(AsiaPollution(1, yr2006:yr2010));

disp(MEPollution(1, yr1991:yr1995));
disp(MEPollution(1, yr1996:yr2000));
disp(MEPollution(1, yr2001:yr2005));
disp(MEPollution(1, yr2006:yr2010));

disp(NAPollution(1, yr1991:yr1995));
disp(NAPollution(1, yr1996:yr2000));
disp(NAPollution(1, yr2001:yr2005));
disp(NAPollution(1, yr2006:yr2010));

disp(LAPollution(1, yr1991:yr1995));
disp(LAPollution(1, yr1996:yr2000));
disp(LAPollution(1, yr2001:yr2005));
disp(LAPollution(1, yr2006:yr2010));

disp(AfricaPollution(1, yr1991:yr1995));
disp(AfricaPollution(1, yr1996:yr2000));
disp(AfricaPollution(1, yr2001:yr2005));
disp(AfricaPollution(1, yr2006:yr2010));

disp(EuroPollution(1, yr1991:yr1995));
disp(EuroPollution(1, yr1996:yr2000));
disp(EuroPollution(1, yr2001:yr2005));
disp(EuroPollution(1, yr2006:yr2010));

disp(AsiaPollution(1, 51:55));
disp(NAPollution(1, 51:55));
disp(EuroPollution(1, 51:55));
disp(MEPollution(1, 51:55));
disp(LAPollution(1, 51:55));
disp(AfricaPollution(1, 51:55));

disp(corrcoef(sentiment_avgs, global_avgs));