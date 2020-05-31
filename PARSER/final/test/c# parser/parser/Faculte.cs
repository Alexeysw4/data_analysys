using System;
using System.Collections.Generic;
using System.Text;

namespace parser
{
    public class Faculte
    {
        public long Id { get; set; }
        public string Name { get; set; }
        public List<PagePerson> PagePersons { get; set; }
        public List<NoPagePerson> NoPagePersons { get; set; }
        public Faculte(long id, string name)
        {
            PagePersons = new List<PagePerson>();
            NoPagePersons = new List<NoPagePerson>();
            Id = id; 
            Name = name;
        }
    }
}
