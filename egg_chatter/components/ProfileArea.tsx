import Image from "next/image";

interface ProfileAreaProps {
    profile : string
}

const ProfileArea = ({ profile = '/assets/logo.png' } : ProfileAreaProps) => {

    return (
        <div className="w-[120px] h-[120px] rounded-full mx-auto my-16">
            
            <Image
                src={profile}
                alt=""
                width={120}
                height={120}
            />
        </div>
    )
}

export default ProfileArea