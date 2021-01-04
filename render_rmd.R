setwd('C:\\Users\\tbeleyur\\Google Drive\\Holger Goerlitz- IMPRS\\PHD_2015\\manuscripts\\Ushichka_dataset')
files <- c('ushichka_dataset.Rmd','ushichka_dataset_supp_info.Rmd')
print('rendering the rmd files....')
for (f in files){rmarkdown::render(f)}