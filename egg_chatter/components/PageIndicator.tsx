interface PageIndicatorProps {
    text :string;
}

const PageIndicator = ({ text } : PageIndicatorProps) => {
    return (
        <p>{text}</p>
    )
}

export default PageIndicator