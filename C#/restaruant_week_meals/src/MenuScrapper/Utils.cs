using System;
using HtmlAgilityPack;

namespace MenuScrapper
{
    public static class Utils
    {
        //Use this method to get HtmlDocument by url (see Constants.cs).
        //HtmlAgilityPack is required

        public static HtmlDocument GetHtmlDoc(string url)
        {
            var web = new HtmlWeb();
            return web.Load(url);
        }

        public static bool IsSameDay(DayOfWeek day1, string day2)
        {
            return day1 switch
            {
                DayOfWeek.Monday when day2.ToLower() == "pondělí" => true,
                DayOfWeek.Tuesday when day2.ToLower() == "úterý" => true,
                DayOfWeek.Wednesday when day2.ToLower() == "středa" => true,
                DayOfWeek.Thursday when day2.ToLower() == "čtvrtek" => true,
                DayOfWeek.Friday when day2.ToLower() == "pátek" => true,
                DayOfWeek.Saturday when day2.ToLower() == "sobota" => true,
                DayOfWeek.Sunday when day2.ToLower() == "neděle" => true,
                _ => false
            };
        }
    }
}
