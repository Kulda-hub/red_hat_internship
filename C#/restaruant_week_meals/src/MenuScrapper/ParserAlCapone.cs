using System.Collections.Generic;
using HtmlAgilityPack;

namespace MenuScrapper
{
    public static class ParserAlCapone
    {
        public static List<DayMenu> Parse(HtmlDocument html)
        {
            var returnList = new List<DayMenu>(); 
            var dadNode = html.DocumentNode.SelectSingleNode("//*[@id=\"wrapper\"]/section[2]/div[1]/div/table/tbody");
            int counter = 0;
            var returnMenu = new DayMenu();
            foreach (var menuNode in dadNode.ChildNodes)
            {
                switch (counter % 12)            // one menu is always in 12 sequence oftable rows 
                {
                 case 1:
                     returnMenu.Day = ParseDay(menuNode);
                     break;
                 
                 case 3:
                     returnMenu.Soup = ParseSoup(menuNode);
                     break;
                 
                 default:
                     if ((counter % 12) % 2 == 0) break;
                     // Console.WriteLine(menuNode.InnerHtml);   
                     returnMenu.Meals.Add(ParseMeal(menuNode));
                     if (counter % 12 == 11)
                     {
                         returnList.Add(new DayMenu(returnMenu));
                         returnMenu = new DayMenu();
                     }
                     break;
                }
                counter++;
            }
            return returnList;
        }

        private static string ParseDay(HtmlNode node)
        {
            return node.ChildNodes[1].InnerText.Trim().Split(" ", 2)[0];
        }
        
        private static string ParseSoup(HtmlNode node)
        {
            return node.ChildNodes[3].InnerText.Trim();
        }
        
        private static Meal ParseMeal(HtmlNode node)
        {
            var returnMeal = new Meal(node.ChildNodes[3].InnerText.Trim())
            {
                Number = int.Parse(node.ChildNodes[1].InnerText.Trim().Split(" ", 2)[1]),
                Price = decimal.Parse(node.ChildNodes[5].InnerText.Trim().Split(",", 2)[0])
            };
            return returnMeal;
        }
    }
}