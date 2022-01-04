data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv")
l = lm(SalePrice~BedroomAbvGr+YearBuilt, data)
#* Predict price of a house
#* @get /predict
function(bedrooms,year,res){
  bedrooms<-as.numeric(bedrooms)
  year<-as.numeric(year)
  if(between(bedrooms,0, 8) & between(year, 1871,2100)){
    X <- data.frame(BedroomAbvGr=bedrooms,YearBuilt=year)
    return(predict(l, newdata = X))
    
  } else {
    res$status <- 400  
    return(list(error = "Please enter BedroomAbvGr between 0 and 8. Enter YearBuilt between 1872 and 2100."))
  }  
}