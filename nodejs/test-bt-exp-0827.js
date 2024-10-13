const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require("@google/generative-ai");
const fs = require('node:fs/promises');
const path = require('path'); // For path manipulation

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

const systemInstruction = { role: "system", parts: [{ text: "" }] };
const generationConfig = {
  temperature: 0.0,
};
const safetySettings = [
  {
    category: HarmCategory.HARM_CATEGORY_HARASSMENT, threshold: HarmBlockThreshold.BLOCK_NONE,
  },
    {
    category: HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold: HarmBlockThreshold.BLOCK_NONE,
  },
    {
    category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold: HarmBlockThreshold.BLOCK_NONE,
  },
    {
    category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold: HarmBlockThreshold.BLOCK_NONE,
  },
];
const apiVersion = 'v1beta';
// https://ai.google.dev/gemini-api/docs/models/gemini
const modelName = 'gemini-1.5-pro-exp-0827';

const mistakes = [
	'<span class="ANAT">aksiyel planda</span> <span class="OBS-P">5 mm kalınlıkta kesitler</span>','aksiyel planda 5 mm kalınlıkta kesitler',
	'<span class="OBS-P">50 ml</span> <span class="OBS-P">noniyonik</span> <span class="OBS-P">kontrast madde</span>','50 ml noniyonik kontrast madde',
	'<span class="OBS-P">noniyonik kontrast madde</span>', 'noniyonik kontrast madde',
	'<span class="OBS-P">noniyonik</span> <span class="OBS-P">kontrast madde</span>', 'noniyonik kontrast madde',
	'<span class="ANAT">aksiyel planda</span> 3 mm <span class="OBS-P">kalınlıkta</span>', 'aksiyel planda 3 mm kalınlıkta',
    '<span class="ANAT">aksiyel planda</span> <span class="OBS-P">3 mm</span> <span class="OBS-P">kalınlıkta</span>', 'aksiyel planda 3 mm kalınlıkta',
	'<span class="ANAT">aksiyel planda</span> <span class="OBS-P">5 mm</span> <span class="OBS-P">kalınlıkta</span>', 'aksiyel planda 5 mm kalınlıkta',
    '<span class="ANAT">aksiyel planda</span> <span class="OBS-P">3 mm kalınlıkta</span>', 'aksiyel planda 3 mm kalınlıkta',
	'<span class="ANAT">aksiyel planda</span> <span class="OBS-P">5 mm kalınlıkta</span>', 'aksiyel planda 5 mm kalınlıkta',
	'<span class="ANAT">aksiyel planda</span> <span class="OBS-P">3 mm</span>', 'aksiyel planda 3 mm',
	'<span class="ANAT">aksiyel planda</span> <span class="OBS-P">5 mm</span>', 'aksiyel planda 5 mm',
	'<span class="OBS-P">kalınlıkta kesitler</span>', 'kalınlıkta kesitler',
	'<span class="ANAT">aksiyel planda</span>', 'aksiyel planda',
	'<span class="IMP">SONUÇ</span>', 'SONUÇ',
	'<span class="IMP">NOT</span>', 'NOT',
	'<span class="ANAT">SONUÇ</span>', 'SONUÇ',
	'<span class="ANAT">NOT</span>', 'NOT',
	'<span class="OBS-P">atelekt</span>azi', '<span class="OBS-P">atelektazi</span>',
	'IV <span class="OBS-P">100 ml</span> noniyonik','IV 100 ml noniyonik',
	'<span class="OBS-P">3 mm</span> <span class="OBS-P">kalınlıkta</span> kesitler',' 3 mm kalınlıkta kesitler',
	'<span class="OBS-P">3 mm kalınlıkta</span> kesitler','3 mm kalınlıkta kesitler',
	'aksiyel planda <span class="OBS-P">3 mm</span> kalınlıkta', 'aksiyel planda 3 mm kalınlıkta',
	'tarihli <span class="ANAT">toraks</span> BT tetkiki ile karşılaştırılarak değerlendirildi','tarihli toraks BT tetkiki ile karşılaştırılarak değerlendirildi',
	'aksiyel planda <span class="OBS-P">5 mm</span> kalınlıkta','aksiyel planda 5 mm kalınlıkta',
	'<span class="OBS-P">5 mm</span> <span class="OBS-P">kalınlıkta</span> kesitler',' 5 mm kalınlıkta kesitler',
	'<span class="OBS-P">60 ml</span> noniyonik kontrast madde','60 ml noniyonik kontrast madde',
	'tarihli <span class="ANAT">toraks</span> BT tetkiki ile karşılaştırılarak','tarihli toraks BT tetkiki ile karşılaştırılarak',
	'<span class="OBS-P">100 ml</span>.noniyonik <span class="OBS-P">kontrast madde</span>','100 ml.noniyonik kontrast madde',
	'tarihli <span class="ANAT">toraks</span> YRBT','tarihli toraks YRBT',
	'<span class="OBS-P">5 mm</span> kalınlığında kesitler','5 mm kalınlığında kesitler',
	'<span class="OBS-P">2 mm</span> kalınlığında MPR','2 mm kalınlığında MPR',
	'iğer BT bulgularda <span class="OBS-A">anlamlı farklılık</span>','BT bulgularda anlamlı farklılık',
	'iğer BT bulgularında <span class="OBS-A">anlamlı farklılık</span>','iğer BT bulgularında anlamlı farklılık',
	'tarihli <span class="ANAT">toraks</span> BT ile','tarihli toraks BT ile',
	'tarihli <span class="ANAT">toraks BT</span> ile','tarihli toraks BT ile',
    ];


async function run() {
    const model = genAI.getGenerativeModel({ model: modelName, generationConfig, safetySettings, systemInstruction,},
     );
    // read prompt
    let prompt;
    try {
        prompt = await fs.readFile('prompt.html', { encoding: 'utf8' });
    } catch (err) {
        console.error(err);
        return; // Exit if prompt reading fails
    }

    // Get list of report files
    const reportsDir = 'reports';
    const files = await fs.readdir(reportsDir);
    const reportFiles = files.filter(file => path.extname(file) === '.txt');

    // Process each report file
    for (const reportFile of reportFiles) {
        const reportPath = path.join(reportsDir, reportFile);
        let report;
        try {
            report = await fs.readFile(reportPath, { encoding: 'utf8' });
        } catch (err) {
            console.error(`Error reading report file ${reportPath}:`, err);
            continue; // Skip to the next file if reading fails
        }

        // Replace double spaces with single spaces in radiology report
        report = report.toString().split('  ').join(' ');
		console.log ("asking report: ", reportFile)
        const result = await model.generateContent(prompt + report);
		const response = await result.response;
		const text = response.text();

		// remove html snippet header and footer, if exists
		const regex = /```html([\s\S]+?)```/g;
		const matches = [];
		let match;
		while ((match = regex.exec(text)) !== null) {
			matches.push(match[1]); // Without trimming whitespace
		}
		let output;
		if (matches.length === 0) {
			output = text;
		} else output = matches;

		// correct frequently made mistakes from array
		for (let i=0; i<mistakes.length; i+=2) {
			output=output.toString().split(mistakes[i]).join(mistakes[i+1]);
		}
        // Construct output file name
        const outputFileName = path.basename(reportFile, '.txt') + '-output.html';
        const outputPath = path.join('outputs', outputFileName);

        // Write output
        await fs.writeFile(outputPath, output, { encoding: 'utf8' }, err => {
            if (err) {
                console.error(`Error writing output file ${outputPath}:`, err);
            }
        });
		// Send next prompt and report to the model with a 1-minute delay
        await new Promise(resolve => setTimeout(resolve, 60 * 1000)); // Delay

        console.log(text);
    }
}

run();