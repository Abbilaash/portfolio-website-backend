/**
 * Google Apps Script for Portfolio Contact Form
 *
 * Instructions:
 * 1. Create a new Google Sheet
 * 2. Create a new Google Apps Script project
 * 3. Replace the default code with this script
 * 4. Update the SHEET_ID constant with your Google Sheet ID
 * 5. Deploy the script as a web app
 * 6. Set execution as "Anyone" and access as "Anyone, even anonymous"
 * 7. Copy the web app URL to your .env file
 */

// Replace with your Google Sheet ID
const SHEET_ID = "1zp2WNk72pwXrta_xZXyh7Gsrr4sTgmTFRdJGFWYK32s";
const SHEET_NAME = "portfolio-website-message";

function doPost(e) {
  try {
    // Parse the JSON data from the request
    const data = JSON.parse(e.postData.contents);

    // Extract the data
    const name = data.name || "";
    const email = data.email || "";
    const message = data.message || "";
    const timestamp = data.timestamp || new Date().toISOString();

    // Log the received data for debugging
    console.log("Received data:", data);
    console.log("Sheet ID:", SHEET_ID);
    console.log("Sheet Name:", SHEET_NAME);

    // Try to open the spreadsheet
    let spreadsheet;
    try {
      spreadsheet = SpreadsheetApp.openById(SHEET_ID);
      console.log("Successfully opened spreadsheet");
    } catch (error) {
      console.error("Failed to open spreadsheet:", error);
      throw new Error(
        "Cannot access the Google Sheet. Check if the Sheet ID is correct and you have access to it."
      );
    }

    // Get or create the sheet
    let sheet = spreadsheet.getSheetByName(SHEET_NAME);

    // If sheet doesn't exist, create it with headers
    if (!sheet) {
      console.log("Sheet does not exist, creating new sheet");
      sheet = spreadsheet.insertSheet(SHEET_NAME);
      sheet
        .getRange(1, 1, 1, 4)
        .setValues([["Timestamp", "Name", "Email", "Message"]]);
      sheet.getRange(1, 1, 1, 4).setFontWeight("bold");
      console.log("Created new sheet with headers");
    } else {
      console.log("Found existing sheet");
    }

    // Append the new row
    const rowData = [timestamp, name, email, message];
    console.log("Appending row:", rowData);

    sheet.appendRow(rowData);
    console.log("Successfully appended row to sheet");

    // Return success response
    return ContentService.createTextOutput(
      JSON.stringify({
        status: "success",
        message: "Data added successfully",
        data: {
          timestamp: timestamp,
          name: name,
          email: email,
          message: message,
          sheetName: SHEET_NAME,
        },
      })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    console.error("Error in doPost:", error);
    // Return error response
    return ContentService.createTextOutput(
      JSON.stringify({
        status: "error",
        message: error.toString(),
        details: "Check the Apps Script logs for more information",
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // Optional: Handle GET requests for testing
  return ContentService.createTextOutput(
    JSON.stringify({
      status: "success",
      message: "Portfolio Contact Form API is working!",
    })
  ).setMimeType(ContentService.MimeType.JSON);
}

// Test function to manually add data
function testAddData() {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    console.log("Successfully opened spreadsheet:", spreadsheet.getName());

    let sheet = spreadsheet.getSheetByName(SHEET_NAME);

    if (!sheet) {
      console.log("Creating new sheet");
      sheet = spreadsheet.insertSheet(SHEET_NAME);
      sheet
        .getRange(1, 1, 1, 4)
        .setValues([["Timestamp", "Name", "Email", "Message"]]);
      sheet.getRange(1, 1, 1, 4).setFontWeight("bold");
    }

    const testData = [
      new Date().toISOString(),
      "Test Name",
      "test@email.com",
      "Test message",
    ];
    sheet.appendRow(testData);
    console.log("Successfully added test data:", testData);
  } catch (error) {
    console.error("Error in testAddData:", error);
  }
}
