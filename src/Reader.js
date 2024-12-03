import React, { useEffect, useState } from 'react';
import { Document, Page } from 'react-pdf';

function Reader() {
    const [pdfFile, setPdfFile] = useState(null);
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    useEffect(() => {
        // 从 URL 获取文件名
        const urlParams = new URLSearchParams(window.location.search);
        const fileName = urlParams.get('file');
        
        if (fileName) {
            // 构建 PDF 文件的 URL
            setPdfFile(`http://127.0.0.1:5000/api/get-pdf/${fileName}`);
        }
    }, []);

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }

    return (
        <div>
            {pdfFile && (
                <Document
                    file={pdfFile}
                    onLoadSuccess={onDocumentLoadSuccess}
                >
                    <Page pageNumber={pageNumber} />
                </Document>
            )}
            <p>
                Page {pageNumber} of {numPages}
            </p>
        </div>
    );
}

export default Reader; 