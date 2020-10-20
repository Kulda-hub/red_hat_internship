using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MenuScrapper
{
    //TODO: Finish Scrapper - implement the load methods for three restaurants.
    public class Scrapper
    {
        public Tuple<string, List<DayMenu>> UDrevaka { get; set; }
        public Tuple<string, List<DayMenu>> AlCapone { get; set; }
        public Tuple<string, List<DayMenu>> UCapa { get; set; }

        public Scrapper()
        {
            LoadAlCapone();
            LoadUCapa();
            LoadUDrevaka();
        }

        private void LoadUDrevaka()
        {
            UDrevaka = Tuple.Create("U Dřeváka Beer & Grill",
                ParserUDreavaka.Parse(Utils.GetHtmlDoc(Constants.udrevakaUrl)));
        }

        private void LoadAlCapone()
        {
            AlCapone = Tuple.Create("Al Capone - Pizzeria Ristorante",
                ParserAlCapone.Parse(Utils.GetHtmlDoc(Constants.alCaponeUrl)));
        }

        private void LoadUCapa()
        {
            UCapa = Tuple.Create("Pivnice u Čápa", ParserUCapa.Parse(Utils.GetHtmlDoc(Constants.uCapaUrl)));
        }
    }
}
