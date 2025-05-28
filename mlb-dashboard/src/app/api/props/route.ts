import { google } from "googleapis";
import { NextResponse } from "next/server";

export async function GET() {
  const sheetId = process.env.GOOGLE_SHEET_ID;
  const clientEmail = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const privateKey = process.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, "\n");

  if (!sheetId || !clientEmail || !privateKey) {
    return new NextResponse("Missing environment variables", { status: 500 });
  }

  const auth = new google.auth.JWT({
    email: clientEmail,
    key: privateKey,
    scopes: ["https://www.googleapis.com/auth/spreadsheets.readonly"],
  });

  const sheets = google.sheets({ version: "v4", auth });

  try {
    const response = await sheets.spreadsheets.values.get({
      spreadsheetId: sheetId,
      range: "Sheet1"
    });

    const [header, ...rows] = response.data.values || [];
    const data = rows.map((row) =>
      Object.fromEntries(header.map((key, i) => [key, row[i] ?? ""]))
    );

    return NextResponse.json(data);
  } catch (error) {
    console.error(error);
    return new NextResponse("Error fetching Google Sheets data", { status: 500 });
  }
}
