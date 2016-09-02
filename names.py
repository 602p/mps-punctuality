TEST_CONSQUENCES=(
	dict(
		name="Test First",
		description="No Punishment",
		trigger="n==1",
		has_consequence=False
	),
	dict(
		name="Test Second",
		description="Fill out Thing",
		trigger="n==2",
		has_consequence=True
	),
	dict(
		name="Third",
		description="Fill out Thing\nGo To Room\nCall Parents",
		trigger="n>2",
		has_consequence=True
	)
)

TEST_TEACHERS="""John Fibnitz
Joe Spuser
Jill Spuser
Foo Bradsher
Bar Foo
Joe Fibnitz""".split("\n")

TEST_REASONS="""Other
Commute
Nurse
Counselor
Other (Excused)""".split("\n")

TEST_NAMES="""Leon Weidenbach  
Kaila Forck  
Mayra Root  
Brigitte Stilwell  
Claribel Hippert  
Tawanda Meis  
Marlen Faries  
Eliseo Denmon  
Wynona Dossantos  
Salvatore Lilley  
Apryl Gazda  
Patty Sautner  
Delphia Chitty  
Mose Fout  
Reina Foland  
Deanne Westcott  
Peg Bertelsen  
Orlando Leonetti  
Marquis Manzer  
Juliet Brewton  
Melita Zermeno  
Pedro Wellington  
Bernie Mailhot  
Gregg Bradsher  
Mona Calo  
Mika Dangerfield  
Mohammad Swinger  
Janella Enos  
Kirstie Gowins  
Polly Hatten  
Gertrud Delfino  
Guadalupe Simkins  
Dale Magno  
Janee Johnston  
Edgar Pavel  
Melia Spiker  
Susana Nelms  
Agatha Krug  
Sherlene Heredia  
Shan Doak  
Rogelio Luong  
Collette Penwell  
Shila Bergey  
Su Pifer  
Holley Haswell  
Teresita Deborde  
Crista Clyburn  
Ilse Spiller  
Lavone Gagne  
Vickey Axtell""".split("\n")