using System;
using System.Collections.Generic;
using System.Text;

namespace parser
{
    public class PagePerson
    {
        public string UrlToPage { get; set; }
        public PagePerson(string urlToPage) 
        {
            UrlToPage = urlToPage;
        }
    }
}
