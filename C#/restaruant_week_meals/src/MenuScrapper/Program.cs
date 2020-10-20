
namespace MenuScrapper
{
    class Program
    {
        static void Main(string[] args)
        {
            var scrapper = new Scrapper();
            var menu = new MenuHandler(scrapper);
        }
    }
}
