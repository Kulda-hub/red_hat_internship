using System.Collections.Generic;
using HtmlAgilityPack;

namespace MenuScrapper
{
    public static class ParserUDreavaka
    {
        public static List<DayMenu> Parse(HtmlDocument html)
        {
            var returnList = new List<DayMenu>(); 
            var dadNode = html.DocumentNode.SelectSingleNode("//*[@id=\"menu\"]/div/div/div/ul");
            foreach (var menuNode in dadNode.Descendants("li"))
            {
                returnList.Add(ParseDayMenu(menuNode));
            }

            return returnList;
        }

        private static DayMenu ParseDayMenu(HtmlNode main)
        {
            var menuNodes = main.Elements("div");
            var returnMenu = new DayMenu();
            returnMenu.Day = main.SelectSingleNode("div[@class = \"menu-day\"]/h3").InnerText;
            int menuNumber = 1;
            foreach (var node in menuNodes)
            {
                switch (node.ChildNodes.Count)     //I did not find a better way to differentiate between nodes with meal
                {                                  //and nodes with other stuff, so that is whz ChildNodes.Count  
                    case 2:
                        break;
                    case 3 when node.ChildNodes[1].InnerText.Contains("Polévka"):
                        returnMenu.Soup = ParseSoupName(node.ChildNodes[1].InnerText);
                        break;
                    case 3:
                        break;
                    default:
                        var returnMeal = new Meal(ParseName(node.ChildNodes[1].InnerText),
                                                ParsePrice(node.ChildNodes[3].InnerText),
                                                menuNumber);
                        menuNumber++;
                        returnMenu.Meals.Add(returnMeal);
                        break;
                }
            }
            return returnMenu;
        }

        private static string ParseName(string text)
        {
            text = text.Trim();
            return text.Split(") ", 2)[1];
        }

        private static decimal ParsePrice(string text)
        {
            return decimal.Parse(text.Split(",")[0]);
        }
        
        private static string ParseSoupName(string text)
        {
            text = text.Trim();
            return text.Split(": ", 2)[1];
        }
    }
}