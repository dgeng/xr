PUT /forex
{
  "mappings": {
     "currency_type" : {
     	"properties" : {
         	"currency": {"type" : "string"},
         	"buying_rate": {"type" : "double"},
         	"cash_buying_rate": {"type" : "double"},
         	"selling_rate": {"type" : "double"},
         	"cach_selling_rate": {"type" : "double"},
         	"middle_rate": {"type" : "double"},
         	"pub_time": {"type" : "date", "format" : "yyyy-MM-dd HH:mm:ss"}
         }
     }
  }
}
