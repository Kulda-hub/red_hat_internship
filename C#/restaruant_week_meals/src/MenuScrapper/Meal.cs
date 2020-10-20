

namespace MenuScrapper
{
    public class Meal
    {
        public int Number { get; set; }
        public string Name { get;}
        public decimal? Price { get; set; }

        public Meal(string name, decimal? price = null, int number = 0)
        {
            Name = name;
            Price = price;
            Number = number;
        }
        
    }
        
}