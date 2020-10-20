using System.Collections.Generic;
using System.Linq;
using HtmlAgilityPack;

namespace MenuScrapper
{
    public static class ParserUCapa
    {
        public static List<DayMenu> Parse(HtmlDocument html)
        {
            var menuNodes =
                html.DocumentNode.SelectNodes(
                    "/html/body/main/div[2]/div/div/div/div/div/div/div[@class = \"row mb-4\"]");
            return menuNodes.Select(menuNode => ParseDayMenu(menuNode)).ToList();
        }

        private static DayMenu ParseDayMenu(HtmlNode node)
        {
            var returnMenu = new DayMenu();
            returnMenu.Day = node.SelectSingleNode("./div/div/div[@class = \"day\" ]").InnerText;
            returnMenu.Soup = node.SelectSingleNode("./div/div[@class = \"row row-polevka\"]/div").InnerText;
            foreach (var mealNode in node.SelectNodes("./div/div[@class = \"row row-food\"]"))
            {
                var splitText = mealNode.SelectSingleNode("./div[contains(@class, 'food')]").InnerText
                    .Split(". ", 2);
                var price = mealNode.SelectSingleNode("./div[contains(@class, 'price')]").InnerText
                    .Split(" K", 2)[0];
                returnMenu.Meals.Add(
                     new Meal(splitText[1], decimal.Parse(price), int.Parse(splitText[0])));
            }
            return returnMenu;
        }
    }
}