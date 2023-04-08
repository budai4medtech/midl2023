# arXiv submission
## 1. Preparation
1. Edit paths and image files paths in `A_copy-tex-figures.bash`

2. Run script to copy tex files and images to arxiv/files path
```
bash A_copy-tex-figures.bash
```
	2.1 Also copy relevant `*.cls` files

3. edit paths for figures  and references in `file\main.tex` as follows
```
%\graphicspath{{../figures}} %goes to path: figures/
\includegraphics[width=\textwidth]{drawing-v01.png}
\includegraphics[width=\linewidth]{drawing-v00.png}
\bibliography{../../references/references}
```

4. compile `main.tex` file
```
cd files/
bash ../B_pdflatex-bibtex.bash
```
Check that reference were appropietely called `evince main.pdf`

	4.1 edit reference section as follows
	```
	%%\bibliography{../references/references}
	\input{main.bbl} %% uncomment for arxiv version
	```

	4.2 compile `main.tex`
	```
	cd files/
	bash ../C_pdflatex-pdflatex.bash
	```

	4.3 check pdf that renders figures and references 
	```
	cd files/
	evince main.pdf
	```

	4.4 clean project 
	```
	cd files/
	bash ../D_clean-tex-project.bash
	```

5. compress it as zip 
```
cd ../
bash E_zip_files.bash v00 # for version 00
bash E_zip_files.bash v01 # for version 01
```
:tada: zip is ready to be submitted in arXiv


6. (Optional) CI-PDF
Create files and edit bib path file
```
cp -r files files-for-ci-pdf
cd files-for-ci-pdf
vim main.tex ## change path for \bibliography
```
Amend yml, adding branch and change relevant paths and filenames for tex and pdf
```
vim .github/workflows/citex.yml
```

## 2. Submission
Login to [arxix](https://arxiv.org/login) and START NEW SUBMISSION with the above zip file
* Click
	* I certify that the above information is correct.   
	* I have read and agree to the Instructions for Submission   
	* By submitting to arXiv I have read and accept the Submission Terms and Agreement  
	* I am submitting as an author of this article  
	* CC BY-SA: Creative Commons Attribution-ShareAlike  
	* Archive and Subject Class: Physics > Medical Physics
	* Continue
* Add files: Add zip `arxiv-v.zip` > Continue: Process Files
* Processing Status: Succeeded! > Continue
* METADATA:
	* title: 
	* author list: : ( Firstname Lastname (where Lastname is your family name).; do not use et al.; separate with commas or 'and'; Review author requirements)
	* abstract.
	* Comments: N pages, N figures
	* Save and continue
* Add other cathegories (for instance):  
	Medical Physics (physics.med-ph)    
	Artificial Intelligence (cs.AI)    Remove
	Hardware Architecture (cs.AR)    Remove
	Machine Learning (cs.LG)    Remove
	Image and Video Processing (eess.IV)  
* You must preview your article before submitting.    
*  Refresh this page after previewing your PDF.   
* Submit: Processing your submission may take several minutes.  
* Maybe you would like to add a [Submission Log](SubmissionLog.md) for further deteails.

## References 
More for metadata: https://arxiv.org/help/prep#title  
