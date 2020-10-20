using System.Collections.Generic;
using System.Text;
namespace MenuScrapper
{
    //This class represents menu of the one day in week.
    public class DayMenu
    {
        public string Day { get; set; }
        public string Soup { get; set; }
        public List<Meal> Meals { get;}

        public DayMenu()
        {
            Meals = new List<Meal>();
        }

        public DayMenu(DayMenu copy)
        {
            Day = copy.Day;
            Soup = copy.Soup;
            Meals = new List<Meal>();
            foreach (var meal in copy.Meals)
            {
                Meals.Add(meal);
            }
        }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.AppendLine(Day)
                    .Append("Polévka: ")
                    .AppendLine(Soup);
            foreach (var meal in Meals)
            {
                builder.Append(meal.Number)
                    .Append(") ")
                    .Append(meal.Name)
                    .Append(" ")
                    .Append('.', 150 - meal.Name.Length)
                    .Append(meal.Price.ToString())
                    .AppendLine(" Kč");
            }
            return builder.ToString();
        }
    }
}
