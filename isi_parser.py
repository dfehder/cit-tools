# Author: DFehder
# Create Date: July 11, 2011
# Purpose: See nbt.org for details
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time, os, random, sys, logging


logging.basicConfig(filename='isi2.log',level=logging.DEBUG)
logging.info("BEGIN RUN")

class isi_parser:
    """
    The purpose of this object is to use selenium to drive downloading of the 
    """
    
    def __init__(self, ):
        """
        Set up the necessary initalization values
        """
        self.base_url = "http://libraries.mit.edu/get/webofsci"

    def waiter(self, phrase):
        def checker():
            cmd = 'wmctrl -l'
            fin,fout = os.popen4(cmd)
            result = fout.read()
            return result

        time.sleep(1)
        n = 0

        for i in range(15):
            if phrase in checker():
                n = 1
                break
            else:
                time.sleep(random.randint(2,3))

        return n
                
            

    def article_grabber2(self, articleList):
        #establish the browser for use across the articles
        browser = webdriver.Firefox() # Get local session of firefox
        browser.get(self.base_url) # Load page

        # I will define three functions in this space
        # these functions will drive try to drive my webpage forward
        # and report if they have succeeded or failed
        # func 1 = art_load

        
        def art_load(artDict, header):
            success = 0
            try:
                elem = browser.find_element_by_id("value(input1)") # Find
                elem.send_keys(artDict[header])
                success = success + 1

                try:
                    elem = browser.find_element_by_id("select1") # Find the dropbox
                    elem.send_keys(header)
                    success = success + 1

                    try:
                        elem = browser.find_element_by_xpath("//input[@alt='Search']")
                        elem.click()
                        test1 = self.waiter("Web of Science Results")
                        if test1 == 1:
                            success = success + 1
                        else:
                            pass

                    except:
                        logging.warning("Search button error  " + artDict[header])                                                   

                except:
                    logging.warning("DOI Search option error  " + artDict[header])
                                      
                                        
            except:
                logging.warning("DOI error  " + artDict[header])

            return success

        def art_sel_save(artDict, header):
            success = 0
            try:
                elem = browser.find_element_by_xpath("//a[@title= 'View all of the articles that cite this one']")
                elem.click()
                test1 = self.waiter("Web of Science Citing Articles")
                if test1 == 1:
                    success = success + 1
                else:
                    pass

                try:
                    # now read the total cite count
                    elem = browser.find_element_by_xpath("//span[@id = 'hitCount.bottom']")
                    boo = elem.text
                    sizeTest = 0
                    if int(boo)>500:
                        #note the size of this in the log
                        logging.info(artDict["DOI"] + "Has more than 500")
                        sizeTest = 1
                    else:
                        pass

                    success = success + 1

                    try:
                        # now put the numbers in for saving
                        elem = browser.find_element_by_xpath("//input[@value='range']")
                        elem.click()
                        elem = browser.find_element_by_xpath("//input[@name = 'markFrom']")
                        elem.send_keys("1")

                        elem = browser.find_element_by_xpath("//input[@name = 'markTo']")
                        if sizeTest == 0:
                            # if less than 500 send number
                            elem.send_keys(boo)
                        else:
                            elem.send_keys("500")

                        elem = browser.find_element_by_xpath("//select[@name='save_options']")
                        elem.send_keys("Save to Tab-delimited (Win)")

                        elem = browser.find_element_by_xpath("//input[@id='fullrec_fields']")
                        elem.click()

                    
                        success = success + 1
                    except:
                        logging.warning("Point 6 Error")
                        
         
                except:
                    logging.warning("Point 5 Error")

                
            except:
                logging.warning("Cited Ref Error")

            return success

        def cit_capture(savePath, fileName, artDict):
            # We have set everything up. Now we just need to click and save
            success = 0
            elem = browser.find_element_by_xpath("//input[@alt='Save the selected records']")
            elem.click()
            # Check to make sure the new webpage loads
            ready1 = self.waiter("Export Transfer Service")

            if ready1 == 1:
                success = success + 1
                try:
                    # check to make sure that the savedrecs popup is in play
                    ready2 = self.waiter("Opening savedrecs.txt")
                    if ready2 == 1:
                        success = success + 1
                        time.sleep(random.randint(2,3))
                        try:
                            #moves the box to the top left of screen
                            os.system("wmctrl -r 'Opening savedrecs.txt' -e 1,0,0,-1,-1")
                            # Now I want to choose the save option
                            os.system("xdotool mousemove 55 230")
                            os.system("xdotool click 1")
                            os.system("xdotool click 1")
                            
                            # These commands do the final clicking to save
                            os.system("xdotool mousemove 370 330")
                            #os.system('xte "key Return"')
                            os.system("xdotool click 1")
                            os.system("xdotool click 1")
                            os.system("xdotool click 1")
                            os.system("xdotool click 1")
                            

                            success = success + 1
                            
                        except:
                            logging.warning("Point 9 Error")
                            return 0
                            
                    else:
                        logging.warning("Point 8 Error")
                        return 0

                    try:
                        #Now we have to save the file in the correct place with the correct name
                        pass

                    except:
                        logging.warning("Point 10 Error")
                        
                except:
                    #stuff
                    logging.warning("Point 11 Error")
            else:
                logging.warning("Point 7 Error")

            # Now we need to make sure that the file is sitting on the desktop
            # if it is, we can then make then move the file to the appropriate place
            try:
                ready3 = 0
                time.sleep(random.randint(1,3))
                
                if os.path.exists(savePath + fileName):
                    ready3 = 1
                else:
                    # error
                    logging.warning("Point 12 Error")
                    

                try:
                    if ready3 == 1:
                        #Now we know the file is there, lets move it and give it the right name
                        stringStart = savePath + fileName
                        #stringStart = 'mv ' + savePath + fileName
                        #stringMid = ' /home/dcfehder/dev/nbt/download/ISI/cf-'
                        #stringMid = ' /home/dcfehder/dev/nbt/download/ISI/cf-'
                        #saveString = stringStart + stringMid + artDict["DOI"][8:] + '.txt'
                        renameString = savePath + "cf-" + artDict["DOI"][8:].strip("\n") + '.txt'
                        
                        # Now rename the file
                        os.rename(stringStart, renameString)
                        # Now move the file
                        

                    else:
                        logging.warning("Point 14 Error")
                  
                    
                    try:
                        #Now we have saved the file to the proper location
                        # it should be gone, so let's check and then
                        # assign a success point if it is
                        if os.path.exists(savePath + fileName):
                            logging.warning("Point 17 Error")
                            
                        else:
                            success = success + 1

                    except:
                        logging.warning("Point 18 Error")

                except:
                    logging.warning("Point 15 Error")
                    
                    
                    

            except:
                logging.warning("Point 13 Error")



            return success

        def returner():
            # the point of this function is to return the user back to the main search page to repeat as necessary
            success = 0

            try:
                elem = browser.find_element_by_xpath("//img[@alt='Return']")
                elem.click()

                ready1 = self.waiter("Web of Science Citing Articles")

                if ready1 == 1:
                    # Now we are back to the citations page
                    # click the search button
                    elem = browser.find_element_by_link_text("Search")
                    elem.click()

                    success = success + 1
                                        
                else:
                    logging.warning("Point 21 Error")
                    

                #next check to make sure that you are on the next page and
                # then you clear the search fields

                try:
                    ready2 = self.waiter("Web of Science Home")
                    if ready2 == 1:
                        # now clear the search fields
                        elem = browser.find_element_by_xpath("//img[@alt='Clear All Search Fields']")
                        elem.click()

                        success = success + 1
                        
                    else:
                        logging.warning("Point 23 Error")

                except:
                    logging.warning("Point 22 Error")
              
                
            except:
                logging.warning("Point 19 Error")

            return success
        
         
    
        # This is where I start the main logic of the function
        # I will now loop through the dictionaries in the list
        for artDict in articleList:

            #check to make sure the page is up
            ready = self.waiter("Web of Science Home")

            # note in the log that you started
            logging.info(artDict["DOI"] + "  Loop begin  " + time.asctime())
            
            if ready == 1:
                pass
            else:
                logging.warning("Failed to Load")
                break


            time.sleep(random.randint(1,3))
            step1 = art_load(artDict, "DOI")
            time.sleep(random.randint(0,3))

            if step1 == 3:
                print "Yeah"
                time.sleep(random.randint(4,6))
                step2 = art_sel_save(artDict, "DOI")
                print step2

                if step2 == 3:
                    print "Yeah 2"
                    time.sleep(random.randint(0,3))
                    step3 = cit_capture("/home/dcfehder/Desktop/","savedrecs.txt", artDict)
                    print step3
                    time.sleep(random.randint(0,3))
                    if step3 == 4:
                        print "Yeah 3"
                        
                        # You wait here because you have the cites
                        # don't want to overload the server
                        time.sleep(random.randint(5,7))
                        step4 = returner()
                        print step4

                        if step4 == 2:
                            # this means you have successfully completed this loop
                            # add some random waiting time and do the next bit
                            time.sleep(random.randint(0,4))

                            logging.info(artDict["DOI"] + "  Loop Successfully ended  " + time.asctime())
                            
                            

                        else:
                            logging.warning("Step 4 Failed")
                            

                    else:
                        logging.warning("Step 3 failed")

                    
                    

                else:
                    logging.warning("Step 2 failed")
             
            else:
                logging.warning("Step 1 failed")
                break

            # close firefox
            
            


