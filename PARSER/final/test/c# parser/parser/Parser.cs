using HtmlAgilityPack;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace parser
{
    public class Parser
    {
        List<Faculte> Facultes { get; set; }

        public Parser()
        {
            Facultes = new List<Faculte>();
            GetFaculties();
            foreach (var faculte in Facultes)
            {
                Console.WriteLine($"Текущий факультет:{faculte.Name}");
                GetPersonsFromFaculte(faculte);
            }
        }

        private void GetFaculties()
        {
            var facultitesPage = new HtmlWeb().Load("https://kpfu.ru/staff/sotrudniki-kfu");

            var aNodes = facultitesPage.DocumentNode.SelectNodes("//li[@class='li_spec']/a");
            foreach (var aNode in aNodes)
            {
                var name = aNode.InnerText;
                var id = aNode.OuterHtml.Split('&')[1].Remove(0, 9);
                Facultes.Add(new Faculte(long.Parse(id), name));
            }
        }

        private void GetPersonsFromFaculte(Faculte faculte)
        {
            Directory.CreateDirectory("data");
            var dataPath = Environment.CurrentDirectory + $"\\data";

            var startUrl = $"https://kpfu.ru/main_page?p_sub=7860&p_id={faculte.Id}&p_order=1&p_page=1";
            bool isNotLastPage = true;

            var currentPath = dataPath + $"\\{faculte.Name}";
            Directory.CreateDirectory(currentPath);

            var linksFilePath = currentPath + $"\\1.txt";
            var linksFile = File.CreateText(linksFilePath);

            var fioFilePath = currentPath + $"\\2.txt";
            var fioFile = File.CreateText(fioFilePath);

            while (isNotLastPage)
            {
                var page = new HtmlWeb().Load(startUrl);

                var allPersons = page.DocumentNode.SelectNodes("//span[@class='fio']");

                if (allPersons == null || allPersons.Count == 0)
                {
                    Console.WriteLine("Страницы кончились");
                    isNotLastPage = false;
                    linksFile.Close();
                    fioFile.Close();
                    return;
                }

                foreach (var person in allPersons)
                {
                    var aTag = person.SelectSingleNode("a");
                    if (aTag != null)
                    {
                        var url = aTag.GetAttributeValue("href", "NotFound");
                        linksFile.Write(url + "\n");
                        faculte.PagePersons.Add(new PagePerson(url)); 
                    }
                    else
                    {
                        var fio = person.InnerText;
                        fioFile.Write(fio + "\n");
                        faculte.NoPagePersons.Add(new NoPagePerson(person.InnerText));
                    }
                }

                int currentPage = int.Parse(startUrl.Split('=').Last());
                currentPage++;
                while (startUrl.Last() != '=')
                {
                    startUrl = startUrl.Remove(startUrl.Length - 1, 1);
                }
                Console.WriteLine($"Переход на страницу{currentPage}"); 
                startUrl += currentPage;
            }
        }
    }
}
