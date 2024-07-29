import React from "react";
import "@/styles/new.css"
import "@/styles/event.css"
import event_image from '@/assets/robocup.jpeg';

// TODO this should be a shadcn ui card component

function LogCard({ event }) {
    return (
            <div className="project-box">
                <img src={event_image} alt='' />
                <div className="event_title">
                    <h3>{event ? event.name : "blabla"}</h3>
                    <div>
                        <button type="button" className="coolbutton">
                            <svg width="4" height="12" viewBox="0 0 4 12" fill="none" xmlns="http://www.w3.org/2000/svg" data-v-6601ed1c="">
                                <circle cx="2" cy="1.5" r="1.5" transform="rotate(90 2 1.5)" fill="hsl(218, 8%, 60%)"></circle>
                                <circle cx="2" cy="6" r="1.5" transform="rotate(90 2 6)" fill="hsl(218, 8%, 60%)"></circle>
                                <circle cx="2" cy="10.5" r="1.5" transform="rotate(90 2 10.5)" fill="hsl(218, 8%, 60%)"></circle>
                            </svg>
                        </button>
                    </div>
                </div>
                <div className="card__section">
                    <div className="attribute-stack" data-v-a53c9a5c="">
                        <div className="attribute-stack__item">
                            <svg data-v-84d60f51="" width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg" className="attribute-stack__icon">
                                <path fillRule="evenodd" clipRule="evenodd" d="M4.97136 1.52205C4.88765 1.49318 4.78347 1.48708 4.35239 1.48708H2.23746C1.91988 1.48708 1.70976 1.48745 1.54865 1.50061C1.39299 1.51333 1.32462 1.53563 1.28304 1.55682C1.16266 1.61815 1.06479 1.71602 1.00345 1.8364C0.982264 1.87798 0.959963 1.94636 0.947245 2.10202C0.934419 2.259 0.933745 2.4625 0.933719 2.76662H5.79792L5.5185 2.20778C5.32572 1.82222 5.27368 1.73175 5.21041 1.66979C5.14266 1.60344 5.06101 1.55297 4.97136 1.52205ZM6.84185 2.76662L6.35364 1.79021C6.34404 1.77101 6.33457 1.75203 6.32521 1.73325C6.17603 1.43414 6.0536 1.18867 5.86375 1.00273C5.69713 0.83953 5.49631 0.715416 5.27582 0.639366C5.0246 0.552715 4.75031 0.55299 4.41606 0.553325C4.39508 0.553346 4.37386 0.553367 4.35239 0.553367L2.21889 0.553367C1.92483 0.553359 1.67629 0.553353 1.47262 0.569994C1.25921 0.58743 1.05428 0.625436 0.859139 0.724867C0.563069 0.875722 0.322356 1.11644 0.1715 1.41251C0.0720698 1.60765 0.0340638 1.81258 0.016628 2.02598C-1.31656e-05 2.22966 -6.96952e-06 2.4782 3.02586e-07 2.77225L4.50997e-07 8.34369C-4.70626e-06 8.79177 -8.89999e-06 9.15634 0.0241664 9.45224C0.0491407 9.75791 0.102224 10.0312 0.231808 10.2855C0.435712 10.6857 0.761071 11.011 1.16125 11.2149C1.41558 11.3445 1.68883 11.3976 1.9945 11.4226C2.29039 11.4467 2.65496 11.4467 3.10304 11.4467H8.89696C9.34504 11.4467 9.70961 11.4467 10.0055 11.4226C10.3112 11.3976 10.5844 11.3445 10.8387 11.2149C11.2389 11.011 11.5643 10.6857 11.7682 10.2855C11.8978 10.0312 11.9509 9.75791 11.9758 9.45224C12 9.15635 12 8.79178 12 8.3437V5.86966C12 5.42158 12 5.05701 11.9758 4.76113C11.9509 4.45546 11.8978 4.1822 11.7682 3.92788C11.5643 3.52769 11.2389 3.20233 10.8387 2.99843C10.5844 2.86885 10.3112 2.81576 10.0055 2.79079C9.7096 2.76661 9.34503 2.76662 8.89694 2.76662L6.84185 2.76662ZM6.54392 3.70034C6.55041 3.70048 6.55692 3.70048 6.56343 3.70034H8.87723C9.34976 3.70034 9.67608 3.7007 9.92946 3.72141C10.1774 3.74166 10.3141 3.77904 10.4148 3.83038C10.6393 3.94476 10.8219 4.12728 10.9362 4.35178C10.9876 4.45253 11.025 4.58923 11.0452 4.83716C11.0659 5.09054 11.0663 5.41686 11.0663 5.88939V8.32397C11.0663 8.7965 11.0659 9.12282 11.0452 9.3762C11.025 9.62413 10.9876 9.76083 10.9362 9.86159C10.8219 10.0861 10.6393 10.2686 10.4148 10.383C10.3141 10.4343 10.1774 10.4717 9.92946 10.492C9.67608 10.5127 9.34976 10.513 8.87723 10.513H3.12277C2.65024 10.513 2.32392 10.5127 2.07054 10.492C1.82261 10.4717 1.68591 10.4343 1.58515 10.383C1.36066 10.2686 1.17814 10.0861 1.06376 9.86159C1.01242 9.76083 0.97504 9.62413 0.954783 9.3762C0.934081 9.12282 0.933718 8.7965 0.933718 8.32397V3.70034H6.54392Z" fill="hsl(0, 0%, 40%)">
                                </path>
                            </svg>
                            <div className="attribute-stack__count">2</div>
                            <div className="attribute-stack__label">Items</div>
                        </div>
                        <div className="attribute-stack__item">
                            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg" className="attribute-stack__icon">
                                <path d="M8.34081 4.87892C9.01445 4.87892 9.56054 4.33283 9.56054 3.65919C9.56054 2.98555 9.01445 2.43946 8.34081 2.43946C7.66717 2.43946 7.12108 2.98555 7.12108 3.65919C7.12108 4.33283 7.66717 4.87892 8.34081 4.87892Z" fill="#5E656E">
                                </path>
                                <path fillRule="evenodd" clipRule="evenodd" d="M4.35157 1.1432C4.77348 0.721291 4.98443 0.510339 5.23061 0.359479C5.44888 0.225726 5.68683 0.127161 5.93575 0.0674025C6.2165 0 6.51483 0 7.1115 0H9.39791C10.3087 0 10.7641 0 11.112 0.177257C11.418 0.333176 11.6668 0.58197 11.8227 0.887979C12 1.23587 12 1.69127 12 2.60209V4.8885C12 5.48517 12 5.7835 11.9326 6.06425C11.8728 6.31317 11.7743 6.55112 11.6405 6.76939C11.4897 7.01557 11.2787 7.22652 10.8568 7.64843L8.2547 10.2505C7.28864 11.2166 6.8056 11.6996 6.24861 11.8806C5.75866 12.0398 5.23089 12.0398 4.74094 11.8806C4.18394 11.6996 3.7009 11.2166 2.73484 10.2505L1.74948 9.26516C0.783409 8.2991 0.300375 7.81606 0.119396 7.25906C-0.0397986 6.76911 -0.0397986 6.24134 0.119396 5.75139C0.300375 5.1944 0.78341 4.71136 1.74948 3.74529L4.35157 1.1432ZM7.1115 1.21973H9.39791C9.87344 1.21973 10.1567 1.22068 10.3667 1.23784C10.4949 1.24831 10.5488 1.26213 10.5632 1.26661C10.6358 1.30486 10.6951 1.36418 10.7334 1.43678C10.7379 1.45122 10.7517 1.5051 10.7622 1.63326C10.7793 1.84326 10.7803 2.12656 10.7803 2.60209V4.8885C10.7803 5.54322 10.7724 5.67179 10.7466 5.77951C10.7167 5.90397 10.6674 6.02295 10.6005 6.13208C10.5426 6.22654 10.4573 6.32299 9.99432 6.78595L7.39222 9.38804C6.89496 9.88531 6.57321 10.2057 6.30887 10.4301C6.05543 10.6453 5.93606 10.6997 5.87169 10.7206C5.62671 10.8002 5.36283 10.8002 5.11785 10.7206C5.05348 10.6997 4.93412 10.6453 4.68067 10.4301C4.41633 10.2057 4.09458 9.88531 3.59732 9.38804L2.61196 8.40268C2.11469 7.90542 1.79428 7.58367 1.56988 7.31933C1.35472 7.06588 1.30034 6.94652 1.27943 6.88215C1.19983 6.63717 1.19983 6.37329 1.27943 6.12831C1.30034 6.06394 1.35472 5.94457 1.56988 5.69113C1.79428 5.42679 2.11469 5.10504 2.61196 4.60777L5.21405 2.00568C5.67701 1.54272 5.77346 1.45736 5.86792 1.39947C5.97705 1.33259 6.09603 1.28331 6.22049 1.25343C6.32821 1.22757 6.45678 1.21973 7.1115 1.21973ZM10.5674 1.26808L10.565 1.26716C10.5667 1.26774 10.5675 1.26806 10.5674 1.26808ZM10.7319 1.43257C10.7319 1.43253 10.7323 1.4333 10.7328 1.43504L10.7319 1.43257Z" fill="#5E656E">
                                </path>
                            </svg>
                            <div className="attribute-stack__count">0</div>
                            <div className="attribute-stack__label">Classes</div>
                        </div>
                    </div>
                </div>
                <div className="card__section progress-section progress">
                    <div role="progressbar" tabIndex="1" className="progress-indicator">
                        <span className="progress-indicator-value progress-indicator-value-active" style={{ width: '55%' }}></span>
                    </div>
                <div className="progress-section-percentage">0%</div></div>
            </div>
    );
}

export default LogCard