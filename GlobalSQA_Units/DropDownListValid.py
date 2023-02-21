import logging
import os
import pandas as pd


from Functions.Functions import ValidateDrpDwnListByXPATH, ROOT_DIR, readfile

Filepath = os.path.join(ROOT_DIR, 'Data', 'DrpList.csv')
df= readfile(Filepath)


def ReadData(rowIndex):
    global Exe
    Exe = df.Exe.values[rowIndex]
    logging.info("Exe: {}".format(Exe))

    global ID
    ID = df.ID.values[rowIndex]
    logging.info("ID: {}".format(ID))

    global PreID
    PreID = df.PreID.values[rowIndex]
    logging.info("PreID: {}".format(PreID))

    global Description
    Description = df.Description.values[rowIndex]
    logging.info("Description: {}".format(Description))

    global Assert
    Assert = df.Assert.values[rowIndex]
    logging.info("Assert: {}".format(Assert))


def Framework():
    if Exe == "P":
        logging.critical("What is happening? (Description) : {}".format(Description))
        logging.info("Do Something with Exe")
    else:
        logging.info("Exit loop Exe != P")
        return

    if pd.notna(Assert):
        logging.info("Do Something with Assert: {}".format(Assert))
        ValidateDrpDwnListByXPATH(
            "//body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/p[1]/select[1]", Assert)


logging.info("****************************************************************************              DRPLIST VALIDATION EXECUTION START              ****************************************************************************")
# Get PreID RowIndex Number to use to speed up lookup for ReadData function.
PreID = sys.argv[0]
y = str(PreID)
#print("PREID TO USE: ", PreID)
logging.info("PREID TO USE: {}".format(PreID))
for i, cell in enumerate(df.PreID.values):
    if cell == y:
        rowIndex = i
        rowindex_print = rowIndex + 1   # this is to account for the two rows on top that are not used / you can tell which tow is running because of this
        ID = df.ID.values[rowIndex]
        # This print is to show where rowIndex x starts - reading data
        logging.info("\n ****** TEST CASE: {} ; TEST DATA ROW INDEX: {} START ****** \n".format(ID, rowindex_print))
        ReadData(rowIndex)
        # This print is to show where rowIndex x ends - reading data
        logging.critical("\n ###### TEST CASE: {} ; TEST DATA ROW INDEX: {} END ###### \n".format(ID, rowindex_print))
        # This print is to show where rowIndex x starts - executing data
        logging.info("\n ****** TEST CASE: {} ; FRAMEWORK ROW INDEX: {} START ****** \n".format(ID, rowindex_print))
        Framework()
        # This print is to show where rowIndex x starts - executing data
        logging.critical("\n ###### TEST CASE: {} ; FRAMEWORK ROW INDEX: {} END ###### \n".format(ID, rowindex_print))
logging.critical("############################################################################               DRPLIST VALIDATION EXECUTION COMPLETE               ############################################################################\n")


